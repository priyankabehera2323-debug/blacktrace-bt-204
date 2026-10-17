
#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
OUTBOX="$ROOT/test-outbox"
REQUEST="$OUTBOX/request.json"

echo "== BlackTrace local prototype reset =="

mkdir -p "$OUTBOX"
chmod 700 "$OUTBOX"

if [[ -e "$REQUEST" ]]; then
    rm -- "$REQUEST"
fi

echo "PASS: local test request cleared"
echo "No live services, inboxes, or proof files were changed."
