
#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"

echo "== BlackTrace setup preflight =="

command -v python3 >/dev/null || {
    echo "FAIL: python3 is missing"
    exit 1
}

python3 -c 'import flask' || {
    echo "FAIL: Flask is missing from system Python"
    exit 1
}

for file in \
    src/request-interface.py \
    src/workflow-prototype.py \
    REQUEST-WORKFLOW.md \
    WORKFLOW-TEST-PLAN.md
do
    test -f "$file" || {
        echo "FAIL: missing $file"
        exit 1
    }
done

id bt-player >/dev/null 2>&1 || {
    echo "FAIL: bt-player account is missing"
    exit 1
}

if sudo -n -l -U bt-player 2>&1 | grep -qi "not allowed"; then
    echo "PASS: bt-player is not allowed to use sudo"
else
    echo "WARNING: review bt-player sudo permissions manually"
fi

echo "PASS: required files and Python dependencies found"
echo "Preflight complete. No services or system files were changed."
