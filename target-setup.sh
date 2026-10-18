#!/usr/bin/env bash
set -euo pipefail
echo "== BlackTrace target preflight =="
if [[ $EUID -ne 0 ]]; then echo "ERROR: Run with sudo on the Ubuntu target."; exit 1; fi
. /etc/os-release
if [[ "${ID:-}" != ubuntu || "${VERSION_ID:-}" != 24.04 ]]; then echo "ERROR: Ubuntu 24.04 required."; exit 1; fi
for p in /opt/blacktrace/app/diagnostics.py /opt/blacktrace/app/records/maintenance-handover.txt /opt/blacktrace/app/records/deployment-checklist.txt /opt/blacktrace/challenge/bin/process-request.py; do [[ -f "$p" ]] || { echo "ERROR: Missing $p"; exit 1; }; done
id bt-player >/dev/null 2>&1 || { echo "ERROR: bt-player missing."; exit 1; }
if id -nG bt-player | tr " " "\n" | grep -Eq "^(sudo|lxd|adm)$"; then echo "ERROR: Administrative group found."; exit 1; fi
echo "PASS: OS, files, and player account verified."
echo "NOTE: Preflight only; no target configuration changed."
