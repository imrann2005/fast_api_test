from flask import Flask, request, jsonify
import logging

app = Flask(__name__)

@app.route('/log', methods=['POST'])
def log_data():
    try:
        data = request.get_json()

        email = data.get('email')
        query = data.get('query')
        

        log_message = f"Received data: user_id={email}, query={query}"

        # Log to console
        print(log_message)

        return jsonify({"status": "logged", "received": data}), 200

    except Exception as e:
       
        return jsonify({"error": "Invalid request"}), 400


@app.route('/process-query', methods=['POST'])
def process_query():
    data = request.json
    print("Webhook received:", data,flush=True)
    return jsonify({"status": "ok","data":data}),200

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)

