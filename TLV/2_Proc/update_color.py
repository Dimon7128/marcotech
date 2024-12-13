from flask import Flask, request
app = Flask(__name__)

@app.route('/update_color', methods=['POST'])
def update_color():
    data = request.get_json()
    color = data.get('color', 'white')
    with open('../DB/DB.txt', 'w') as file:
        file.write(color)
    return '', 204
