
#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"

echo "== BlackTrace local prototype setup =="

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
    src/safe-review-processor.py \
    REQUEST-WORKFLOW.md \
    WORKFLOW-TEST-PLAN.md \
    health-check.sh \
    reset.sh
do
    if [[ ! -f "$file" ]]; then
        echo "FAIL: missing $file"
        exit 1
    fi
done

python3 -m py_compile \
    src/request-interface.py \
    src/workflow-prototype.py \
    src/safe-review-processor.py

mkdir -p test-outbox
chmod 700 test-outbox

echo "PASS: Python and Flask available"
echo "PASS: all required prototype files exist"
echo "PASS: Python syntax checks passed"
echo "PASS: local test outbox is ready"
echo "NOTE: this script does not deploy or activate the live CTF."
