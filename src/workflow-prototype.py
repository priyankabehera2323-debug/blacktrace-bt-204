#!/usr/bin/env python3
"""BlackTrace local workflow prototype; no privileged actions."""

import json
from pathlib import Path
from flask import Flask, jsonify, request

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 2048

OUTBOX = Path(__file__).resolve().parents[1] / "test-outbox"
OUTBOX.mkdir(mode=0o700, parents=True, exist_ok=True)
OUTBOX.chmod(0o700)

@app.get("/health")
def health():
    return jsonify(service="blacktrace-workflow-prototype", status="ok")

@app.post("/submit")
def submit():
    if not request.is_json:
        return jsonify(error="Content-Type must be application/json"), 415

    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify(error="JSON object required"), 400

    if data.get("ticket") != "BT-204":
        return jsonify(error="Unknown ticket"), 400

    action = data.get("action")
    if action not in ("review", "status-check"):
        return jsonify(error="Unsupported action"), 400

    record = {"ticket": "BT-204", "action": action}
    path = OUTBOX / "request.json"
    path.write_text(json.dumps(record) + "\n", encoding="utf-8")
    path.chmod(0o600)

    return jsonify(status="accepted", ticket="BT-204"), 202

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8081, debug=False)
