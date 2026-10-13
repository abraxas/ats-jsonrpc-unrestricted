#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
export COMPOSE_PROJECT_NAME="${COMPOSE_PROJECT_NAME:-ats-jsonrpc-unrestricted}"
export PYTHONUNBUFFERED=1

LABEL="ats-jsonrpc-unrestricted"
WITNESS="ATS-JSONRPC-UNRESTRICTED-WITNESS"
IMAGE_TAG="ats-10.2.0-lab:local"
LOCK_PATH="/tmp/ats-10.2.0-lab.lock"
SRC_STAGE="/tmp/ats-10.2.0-src"
HTTP_URL="http://127.0.0.1:18720/"

down() {
  echo "== docker compose down -v =="
  docker compose -p "${COMPOSE_PROJECT_NAME}" down -v --remove-orphans || true
}

fail_setup() {
  local reason="$1"
  echo "FAIL ${LABEL} ${reason} ${WITNESS}" | tee poc-last-run.txt
  down
  exit 1
}

ensure_shared_image() {
  echo "== ensure ${IMAGE_TAG} =="
  if docker image inspect "${IMAGE_TAG}" >/dev/null 2>&1; then
    echo "IOC shared-image-present ${IMAGE_TAG}"
    return 0
  fi
  echo "== ${IMAGE_TAG} missing; lock ${LOCK_PATH} and build =="
  python3 - "${LOCK_PATH}" "${IMAGE_TAG}" "${SRC_STAGE}" Dockerfile.base <<'PY' \
    || fail_setup "shared-image-build-failed"
import fcntl
import os
import subprocess
import sys
from pathlib import Path

lock_path, image, src_stage, dockerfile_base = sys.argv[1:5]
here = Path.cwd()
src_tree = os.environ.get("ATS_SRC")
if not src_tree:
    src_tree = str((here / "../../client-reviews/trafficserver/src").resolve())

Path(lock_path).touch()
with open(lock_path, "a", encoding="utf-8") as lock:
    fcntl.flock(lock.fileno(), fcntl.LOCK_EX)
    inspect = subprocess.run(
        ["docker", "image", "inspect", image],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    if inspect.returncode == 0:
        print(f"IOC shared-image-present {image}", flush=True)
        raise SystemExit(0)
    if not Path(src_tree, "CMakeLists.txt").is_file():
        print("ats-src-missing", file=sys.stderr)
        raise SystemExit(1)
    print(f"== rsync ATS 10.2.0 source -> {src_stage} ==", flush=True)
    Path(src_stage).mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [
            "rsync", "-a", "--delete",
            "--exclude", ".git",
            "--exclude", "doc",
            "--exclude", "tests",
            "--exclude", "ci",
            f"{src_tree}/",
            f"{src_stage}/",
        ],
        check=True,
    )
    staged = Path(src_stage, "Dockerfile.base")
    if not staged.is_file():
        staged.write_bytes(Path(dockerfile_base).read_bytes())
    print(f"== docker build {image} ==", flush=True)
    subprocess.run(
        ["docker", "build", "-t", image, "-f", str(staged), src_stage],
        check=True,
    )
    subprocess.run(["docker", "image", "inspect", image], check=True, stdout=subprocess.DEVNULL)
PY
}

trap down EXIT

echo "== docker compose down (clean) =="
down

ensure_shared_image

echo "== docker compose up --build =="
up_ok=0
for attempt in $(seq 1 8); do
  if docker compose -p "${COMPOSE_PROJECT_NAME}" up --build -d; then
    up_ok=1
    break
  fi
  echo "compose-up-retry attempt=${attempt}"
  sleep 12
  down
done
if [[ "${up_ok}" != 1 ]]; then
  fail_setup "compose-up-failed"
fi

echo "== wait ${HTTP_URL} =="
ok=0
for i in $(seq 1 90); do
  if python3 - <<'PY'
import urllib.error
import urllib.request

req = urllib.request.Request(
    "http://127.0.0.1:18720/",
    headers={"Host": "127.0.0.1:8080"},
    method="GET",
)
try:
    with urllib.request.urlopen(req, timeout=3) as resp:
        body = resp.read().decode("utf-8", "replace")
        raise SystemExit(0 if resp.status == 200 else 1)
except (urllib.error.URLError, TimeoutError, OSError):
    raise SystemExit(1)
PY
  then
    ok=1
    echo "ats-ready attempt=${i}"
    break
  fi
  echo "ats-wait attempt=${i}"
  sleep 2
done
if [[ "${ok}" != 1 ]]; then
  echo "== compose logs (not ready) =="
  docker compose -p "${COMPOSE_PROJECT_NAME}" logs --no-color --tail=160 || true
  fail_setup "ats-not-ready"
fi

echo "== poc.py =="
set +e
python3 ./poc.py | tee poc-last-run.txt
rc=${PIPESTATUS[0]}
set -e

if ! tail -n1 poc-last-run.txt 2>/dev/null | grep -qE '^(SUCCESS|FAIL) '; then
  echo "FAIL ${LABEL} poc-exit=${rc} ${WITNESS}" >> poc-last-run.txt
  rc=1
fi

exit "${rc}"
