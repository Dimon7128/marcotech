from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

data = [{"id": 1, "item": "Sample Item"}]

@app.route('/data', methods=['GET'])
def get_data():
    return jsonify(data), 200

@app.route('/data', methods=['POST'])
def post_data():
    new_item = {
        "id": len(data) + 1,
        "item": request.json.get("item")
    }
    data.append(new_item)
    return jsonify(new_item), 201

@app.route('/data/<int:item_id>', methods=['PUT'])
def put_data(item_id):
    for item in data:
        if item['id'] == item_id:
            item['item'] = request.json.get("item")
            return jsonify(item), 200
    return jsonify({"error": "Item not found"}), 404

@app.route('/data/<int:item_id>', methods=['DELETE'])
def delete_data(item_id):
    global data
    data = [item for item in data if item['id'] != item_id]
    return jsonify({"message": "Item deleted"}), 200

if __name__ == '__main__':
    app.run(debug=True)
