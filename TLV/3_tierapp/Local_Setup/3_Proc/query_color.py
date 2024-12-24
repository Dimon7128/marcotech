import time
from flask import Flask, jsonify, request
import csv
import threading

app = Flask(__name__)
db_file = "../DB/DB.csv"  # Use an absolute path
current_color = "white"
lock = threading.Lock()

# Periodically read the color from the DB
def read_color_periodically():
    global current_color
    while True:
        try:
            with open(db_file, 'r') as file:
                reader = csv.reader(file)
                color = next(reader)[0]
                with lock:
                    if color != current_color:
                        current_color = color
        except Exception as e:
            print(f"Error reading DB.csv: {e}")
        time.sleep(20)

# Endpoint to fetch the current color
@app.route('/api/get_color', methods=['GET'])
def get_color():
    with lock:
        return jsonify({'color': current_color})

# Endpoint to update the color in the DB
@app.route('/api/update_color', methods=['POST'])
def update_color():
    global current_color
    data = request.get_json()
    color = data.get('color', 'white')
    with open(db_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([color])
    with lock:
        current_color = color
    return '', 204

# Start the periodic background thread
if __name__ == "__main__":
    threading.Thread(target=read_color_periodically, daemon=True).start()
    app.run(port=5002, debug=True)
