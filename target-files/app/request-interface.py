#!/usr/bin/env python3
"""BlackTrace maintenance request API; validates input and stores requests."""

import json
import os
import tempfile
from pathlib import Path

from flask import Flask, jsonify, request

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 2048

INBOX = Path("/var/lib/blacktrace/inbox")
ALLOWED_ACTIONS = {"review", "status-check", "profile-check"}
ALLOWED_PROFILE = "NIGHTJAR-17"


@app.get("/health")
def health():
    return jsonify(service="blacktrace-request-interface", status="ok")


@app.post("/submit")
def submit():
    if not request.is_json:
        return jsonify(error="Content-Type must be application/json"), 415

    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify(error="JSON object required"), 400

    if data.get("ticket") != "BT-204":
        return jsonify(error="Unknown maintenance ticket"), 400

    action = data.get("action")
    if not isinstance(action, str) or action not in ALLOWED_ACTIONS:
        return jsonify(error="Unsupported action"), 400

    INBOX.mkdir(mode=0o750, parents=True, exist_ok=True)
    reviewer = data.get("reviewer")
    if reviewer is not None and not isinstance(reviewer, str):
        return jsonify(error="Reviewer must be a string"), 400

    payload = {
        "ticket": "BT-204",
        "action": action,
    }
    if action == "profile-check":
        profile = data.get("profile")
        if profile != ALLOWED_PROFILE:
            return jsonify(error="Unknown workflow profile"), 403
        payload["profile"] = profile
    if reviewer is not None:
        payload["reviewer"] = reviewer

    fd, temporary = tempfile.mkstemp(prefix=".request-", dir=INBOX)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(payload, handle)
            handle.write("\n")
        os.chmod(temporary, 0o640)
        os.replace(temporary, INBOX / "request.json")
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)

    return jsonify(
        status="accepted",
        ticket="BT-204",
        message="Request saved for review; no privileged action was run.",
    ), 202


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8081, debug=False)
