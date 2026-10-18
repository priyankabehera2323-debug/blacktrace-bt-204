#!/usr/bin/env bash
set -u

fail=0

check() {
    if "$@"; then
        echo "PASS: $*"
    else
        echo "FAIL: $*"
        fail=1
    fi
}

check systemctl is-active --quiet blacktrace-diagnostics.service
check systemctl is-active --quiet blacktrace-request-interface.service

check test -f /opt/blacktrace/app/diagnostics.py
check test -f /opt/blacktrace/app/request-interface.py
check test -f /opt/blacktrace/app/records/maintenance-handover.txt
check test -f /opt/blacktrace/app/records/deployment-checklist.txt

check test -x /opt/blacktrace/challenge/bin/process-request.py
check test -r /opt/blacktrace/challenge/bin/review_policy.py
check test -f /etc/systemd/system/blacktrace-review.service
check test -f /etc/systemd/system/blacktrace-review.timer

check id bt-player
check id bt-operator
check test -f /root/blacktrace/proof.txt
check test "$(stat -c '%U:%G:%a' /root/blacktrace/proof.txt)" = "root:root:600"

if (( fail )); then
    echo "Health check failed."
    exit 1
fi

echo "PASS: target prerequisites look healthy."
echo "NOTE: full challenge behavior still requires an isolated end-to-end test."
