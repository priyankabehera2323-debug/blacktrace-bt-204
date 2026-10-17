
#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"

echo "== BlackTrace build health check =="

command -v python3 >/dev/null
python3 -c 'import flask'

for file in \
    src/request-interface.py \
    src/workflow-prototype.py \
    src/safe-review-processor.py \
    REQUEST-WORKFLOW.md \
    WORKFLOW-TEST-PLAN.md
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

test -d test-outbox || {
    echo "FAIL: test-outbox missing"
    exit 1
}

echo "PASS: Python and Flask available"
echo "PASS: required source and documentation exist"
echo "PASS: Python syntax checks passed"
echo "PASS: local test outbox exists"
echo "Note: this checks the build workspace, not live-target deployment."
