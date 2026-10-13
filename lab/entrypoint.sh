#!/usr/bin/env bash
set -euo pipefail

export PATH="/opt/ats/bin:${PATH}"

mkdir -p /opt/ats/var/trafficserver /opt/ats/var/log/trafficserver /opt/lab/origin
chown nobody:nogroup /opt/ats/var/trafficserver /opt/ats/var/log/trafficserver
chmod 0755 /opt/ats/var/trafficserver /opt/ats/var/log/trafficserver

python3 -m http.server 18080 --bind 127.0.0.1 --directory /opt/lab/origin \
    >/tmp/origin.log 2>&1 &

exec traffic_server
