
#!/usr/bin/env python3
"""BlackTrace local-only request interface; no privileged actions."""

import json
import os
import tempfile
from pathlib import Path

from flask import Flask, jsonify, request

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 2048

OUTBOX = Path(__file__).resolve().parents[1] / "test-outbox"
ALLOWED_ACTIONS = {"review", "status-check"}


@app.get("/health")
def health():
    return jsonify(service="blacktrace-request-interface", status="ok")


@app.post("/submit")
def submit():
    if not request.is_json:
        return jsonify(error="Content-Type must be application/json"), 415

    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify(error="A JSON object is required"), 400

    if data.get("ticket") != "BT-204":
        return jsonify(error="Unknown maintenance ticket"), 400

    action = data.get("action")
    if not isinstance(action, str) or action not in ALLOWED_ACTIONS:
        return jsonify(error="Unsupported action"), 400

    OUTBOX.mkdir(mode=0o700, parents=True, exist_ok=True)
    OUTBOX.chmod(0o700)

    payload = {"ticket": "BT-204", "action": action}
    fd, temporary = tempfile.mkstemp(prefix=".request-", dir=OUTBOX)

    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(payload, handle)
            handle.write("\n")
        os.chmod(temporary, 0o600)
        os.replace(temporary, OUTBOX / "request.json")
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)

    return jsonify(
        status="accepted",
        ticket="BT-204",
        message="Saved to the local test outbox; no privileged workflow was triggered.",
    ), 202


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8081, debug=False)
