#!/usr/bin/env python3
"""BlackTrace BT-204 request-interface prototype."""

from flask import Flask, jsonify, request

app = Flask(__name__)

MAX_CONTENT_LENGTH = 2048
app.config["MAX_CONTENT_LENGTH"] = MAX_CONTENT_LENGTH

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

    ticket = data.get("ticket")
    action = data.get("action")

    if ticket != "BT-204":
        return jsonify(error="Unknown maintenance ticket"), 400

    if not isinstance(action, str) or action not in {
        "review",
        "status-check",
    }:
        return jsonify(error="Unsupported action"), 400

    # Prototype only: do not write to the privileged inbox or run commands.
    app.logger.info("Accepted prototype request for ticket %s", ticket)
    return jsonify(
        status="accepted",
        ticket=ticket,
        message="Prototype request validated; no workflow was triggered.",
    ), 202


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8081, debug=False)
