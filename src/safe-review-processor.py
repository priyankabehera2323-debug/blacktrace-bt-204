
#!/usr/bin/env python3
"""BlackTrace safe review-processor prototype.

Local test only: no privileged actions or shell execution.
"""

import json
import sys
from pathlib import Path
from datetime import datetime, timezone

BASE_DIR = Path(__file__).resolve().parents[1]
TEST_OUTBOX = BASE_DIR / "test-outbox"
AUDIT_FILE = TEST_OUTBOX / "review-audit.jsonl"
ALLOWED_ACTIONS = {"review", "status-check"}


def main():
    request_file = TEST_OUTBOX / "request.json"

    if not request_file.is_file():
        print("No pending test request.")
        return 1

    try:
        data = json.loads(request_file.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        print("Invalid request file.")
        return 1

    if not isinstance(data, dict):
        print("Request must be a JSON object.")
        return 1

    ticket = data.get("ticket")
    action = data.get("action")

    if ticket != "BT-204":
        print("Rejected: unknown ticket.")
        return 1

    if not isinstance(action, str) or action not in ALLOWED_ACTIONS:
        print("Rejected: unsupported action.")
        return 1

    result = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "ticket": ticket,
        "action": action,
        "result": "reviewed",
    }

    TEST_OUTBOX.mkdir(mode=0o700, parents=True, exist_ok=True)
    TEST_OUTBOX.chmod(0o700)

    with AUDIT_FILE.open("a", encoding="utf-8") as audit:
        audit.write(json.dumps(result) + "\n")

    AUDIT_FILE.chmod(0o600)
    print(f"Reviewed ticket: {ticket}; action: {action}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
