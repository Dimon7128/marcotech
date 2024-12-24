from flask import Flask, request, jsonify
from flask_cors import CORS
import csv

app = Flask(__name__)
CORS(app)

db_file = "DB/DB.csv"  # Make sure this path is correct

@app.route('/api/update_color', methods=['POST'])
def update_color():
    try:
        data = request.get_json()
        color = data.get('color', 'white')
        with open(db_file, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([color])
        return jsonify({'status': 'success'}), 200
    except Exception as e:
        print(f"Error updating color: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/get_color', methods=['GET'])
def get_color():
    try:
        with open(db_file, 'r') as file:
            reader = csv.reader(file)
            color = next(reader)[0]
            return jsonify({'color': color})
    except Exception as e:
        print(f"Error reading color: {e}")
        return jsonify({'color': 'white'})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)