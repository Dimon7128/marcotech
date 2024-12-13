import time
from flask import Flask, jsonify

app = Flask(__name__)
current_color = "white"

def read_color_periodically():
    global current_color
    while True:
        try:
            with open('../DB/DB.txt', 'r') as file:
                current_color = file.read().strip()
        except FileNotFoundError:
            pass
        time.sleep(60)

@app.route('/get_color', methods=['GET'])
def get_color():
    return jsonify({'color': current_color})

# Start the periodic updater in a separate thread or as a background task.
import threading
threading.Thread(target=read_color_periodically, daemon=True).start()
