#!/usr/bin/env python3
"""BlackTrace BT-204 privileged review workflow."""

import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

from review_policy import validate_request

REQUEST = Path(os.environ.get(
    "BLACKTRACE_REQUEST", "/var/lib/blacktrace/inbox/request.json"
))
AUDIT = Path(os.environ.get(
    "BLACKTRACE_AUDIT", "/var/log/blacktrace/review-audit.jsonl"
))
REPORT = Path(os.environ.get(
    "BLACKTRACE_REPORT", "/var/lib/blacktrace/reports/BT-204-review.txt"
))


def main():
    try:
        data = json.loads(REQUEST.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        print("No valid pending request.")
        return 1

    allowed, reason = validate_request(data)
    if not allowed:
        print(f"Rejected: {reason}")
        return 1

    record = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "ticket": data["ticket"],
        "action": data["action"],
        "reviewer": data["reviewer"],
        "result": "reviewed",
    }

    try:
        AUDIT.parent.mkdir(parents=True, exist_ok=True)
        with AUDIT.open("a", encoding="utf-8") as audit:
            audit.write(json.dumps(record) + "\n")

        if data["action"] == "profile-check":
            if data.get("profile") != "NIGHTJAR-17":
                print("Rejected: workflow profile is not authorized")
                return 1
            REPORT.parent.mkdir(parents=True, exist_ok=True)
            REPORT.write_text(
                "BlackTrace BT-204 profile check complete\n"
                "Profile: NIGHTJAR-17\n"
                "Result: configuration verified\n",
                encoding="utf-8",
            )
            REPORT.chmod(0o640)
        elif data["action"] == "review":
            REPORT.parent.mkdir(parents=True, exist_ok=True)
            REPORT.write_text(
                "BlackTrace BT-204 review complete\n"
                "Result: reviewed\n"
                "Proof: retained in protected storage\n",
                encoding="utf-8",
            )
            REPORT.chmod(0o640)

        REQUEST.unlink(missing_ok=True)
    except (OSError, KeyError) as exc:
        print(f"Review failed: {exc}")
        return 1

    print(f"Reviewed ticket: {data['ticket']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
