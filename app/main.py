from flask import Flask, request, jsonify
import os
import json
from datetime import datetime

app = Flask(__name__)

# Constants
DATA_DIR = "data"
DATA_FILE = os.path.join(DATA_DIR, "requests.jsonl")

# Ensure data directory exists
os.makedirs(DATA_DIR, exist_ok=True)

@app.route('/process-query', methods=['POST'])
def save_data():
    try:
        data = request.get_json()
     

        timestamp = datetime.now().isoformat()
        entry = {
            "timestamp": timestamp,
            "data" : data
        }

        # Save to file as JSONL
        with open(DATA_FILE, "a") as f:
            f.write(json.dumps(entry) + "\n")

        return jsonify({"status": "saved", "entry": entry}), 200

    except Exception as e:
        return jsonify({"error": "Invalid request", "details": str(e)}), 400

@app.route('/view-data', methods=['GET'])
def view_data():
    if not os.path.exists(DATA_FILE):
        return jsonify({"error": "No data file found"}), 404

    entries = []
    with open(DATA_FILE, "r") as f:
        for line in f:
            try:
                entries.append(json.loads(line.strip()))
            except json.JSONDecodeError:
                continue

    return jsonify({"count": len(entries), "entries": entries}), 200

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
