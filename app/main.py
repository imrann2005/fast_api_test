from flask import Flask, request, jsonify
import os
from datetime import datetime
import logging

app = Flask(__name__)

# Create a logs directory if it doesn't exist
os.makedirs("logs", exist_ok=True)

# Configure logging to file
logging.basicConfig(
    filename="logs/api_requests.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

@app.route('/log', methods=['POST'])
def log_data():
    try:
        data = request.get_json()

        email = data.get('email')
        query = data.get('query')

        log_message = f"Received data: user_id={email}, query={query}"

        # Log to console (visible in Render)
        print(log_message, flush=True)

        # Also log to file
        logging.info(log_message)

        return jsonify({"status": "logged", "received": data}), 200

    except Exception as e:
        logging.error(f"Error in /log: {str(e)}")
        return jsonify({"error": "Invalid request"}), 400

@app.route('/process-query', methods=['POST'])
def process_query():
    data = request.json
    logging.info(f"Data from /process-query: {data}")
    return jsonify({"status": "ok", "data": data}), 200

@app.route('/view-log', methods=['GET'])
def view_log():
    log_file = "logs/api_requests.log"

    if not os.path.exists(log_file):
        return jsonify({"error": "Log file does not exist"}), 404

    with open(log_file, "r") as file:
        content = file.read()

    return jsonify({"log": content}), 200

# Optional: log every request method and path
@app.before_request
def log_all_requests():
    print(f"[{datetime.now()}] 🔄 {request.method} {request.path}", flush=True)

if __name__ == '__main__':
    # Use dynamic port binding for Render compatibility
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
