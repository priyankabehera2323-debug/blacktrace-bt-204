from pathlib import Path
from flask import Flask, jsonify, abort

app = Flask(__name__)

RECORDS_DIR = Path(__file__).resolve().parent / "records"

@app.get("/")
def index():
    return """
    <!doctype html>
    <html lang="en">
    <head><title>BlackTrace Diagnostics</title></head>
    <body>
      <h1>BlackTrace Diagnostics</h1>
      <p>Internal maintenance diagnostics.</p>
      <p>Service status: operational</p>
      <p>Reference: BT-204</p>
      <p>Records index: /records</p>
    </body>
    </html>
    """

@app.get("/health")
def health():
    return jsonify(status="ok", service="diagnostics")

@app.get("/api/diagnostics")
def diagnostics():
    return jsonify(
        service="blacktrace-diagnostics",
        status="operational",
        maintenance_ticket="BT-204",
        note="Review the maintenance team's handover records."
    )

@app.get("/records")
def records_index():
    return jsonify(
        records=[
            "maintenance-handover.txt",
            "deployment-checklist.txt"
        ]
    )

@app.get("/records/<filename>")
def get_record(filename):
    allowed = {
        "maintenance-handover.txt",
        "deployment-checklist.txt"
    }
    if filename not in allowed:
        abort(404)

    path = RECORDS_DIR / filename
    if not path.is_file():
        abort(404)

    return path.read_text(), 200, {"Content-Type": "text/plain; charset=utf-8"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=False)
