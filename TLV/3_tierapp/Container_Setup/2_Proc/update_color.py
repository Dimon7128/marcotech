from flask import Flask, request, jsonify
from flask_cors import CORS
import csv
import os

app = Flask(__name__)
CORS(app)

db_file = "DB/DB.csv"  # Make sure this path is correct
CSV_PATH = 'DB/not_allowed.csv'

def read_not_allowed_colors():
    if not os.path.exists(CSV_PATH):
        return []
    with open(CSV_PATH, 'r') as file:
        reader = csv.reader(file)
        return [row[0] for row in reader]

def write_not_allowed_colors(colors):
    with open(CSV_PATH, 'w', newline='') as file:
        writer = csv.writer(file)
        for color in colors:
            writer.writerow([color])

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

@app.route('/update_not_allowed_csv', methods=['POST'])
def update_not_allowed_csv():
    try:
        data = request.get_json()
        colors = data.get('colors', [])
        write_not_allowed_colors(colors)
        return jsonify({"status": "success", "message": "Colors updated successfully"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/get_not_allowed_csv', methods=['GET'])
def get_not_allowed_csv():
    try:
        colors = read_not_allowed_colors()
        return jsonify({"status": "success", "colors": colors})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)