from flask import Flask, request
import csv

app = Flask(__name__)
db_file = "DB/DB.csv"

@app.route('/api/update_color', methods=['POST'])
def update_color():
    data = request.get_json()
    color = data.get('color', 'white')
    with open(db_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([color])
    return '', 204

if __name__ == "__main__":
    app.run(port=5001, debug=False)
