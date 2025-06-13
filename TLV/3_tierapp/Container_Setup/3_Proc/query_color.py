from flask import Flask, jsonify
from flask_cors import CORS
import requests
import time
import os

app = Flask(__name__)
CORS(app)

# Get the IP from environment variable
backend_vm2_api = f"http://{os.environ.get('UPDATE_COLOR_SERVICE', 'localhost')}:5001/api/get_color"

@app.route('/api/get_color', methods=['GET'])
def get_color():
    try:
        # Add 10 second delay
        time.sleep(10)
        
        response = requests.get(backend_vm2_api, timeout=5)
        response.raise_for_status()
        return jsonify(response.json())
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to Backend VM2: {e}")
        return jsonify({'color': 'white'})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5002, debug=False)