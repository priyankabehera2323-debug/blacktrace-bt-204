
#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
OUTBOX="$ROOT/test-outbox"

echo "== BlackTrace local prototype reset =="

mkdir -p "$OUTBOX"
chmod 700 "$OUTBOX"

for file in request.json review-audit.jsonl; do
    if [[ -e "$OUTBOX/$file" ]]; then
        rm -- "$OUTBOX/$file"
    fi
done

echo "PASS: local request and audit log cleared"
echo "No live services, privileged inboxes, proof files, or Wazuh settings were changed."
