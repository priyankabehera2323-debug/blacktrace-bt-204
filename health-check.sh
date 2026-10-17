#!/usr/bin/env bash
set -euo pipefail
echo "== BlackTrace health check =="
id bt-player
if sudo -n -l -U bt-player 2>&1 | grep -qi "not allowed"; then
  echo "PASS: bt-player has no sudo permission"
else
  echo "CHECK: review bt-player sudo permissions manually"
fi
sudo test -f /root/blacktrace-proof.txt
sudo test "$(sudo stat -c '%U:%G:%a' /root/blacktrace-proof.txt)" = "root:root:600"
echo "PASS: root proof file exists with root:root mode 600"
echo "PASS: basic checks complete"
