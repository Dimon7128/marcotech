from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

# VM2's address where the CSV file is located
VM2_BASE_URL = 'http://<IP_update_color>:5001'  # Update with VM2's actual IP

@app.route('/api/update_not_allowed', methods=['POST'])
def update_not_allowed():
    try:
        data = request.get_json()
        # Forward the request to VM2
        response = requests.post(f'{VM2_BASE_URL}/update_not_allowed_csv', json=data)
        return jsonify(response.json())
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/get_not_allowed', methods=['GET'])
def get_not_allowed():
    try:
        # Get the data from VM2
        response = requests.get(f'{VM2_BASE_URL}/get_not_allowed_csv')
        return jsonify(response.json())
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003) 