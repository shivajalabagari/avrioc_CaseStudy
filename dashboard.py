from flask import Flask, jsonify
from pymongo import MongoClient

app = Flask(__name__)
mongo_client = MongoClient("mongodb://localhost:27017")
db = mongo_client["analytics"]
collection = db["aggregated_interactions"]

@app.route('/metrics', methods=['GET'])
def get_metrics():
    data = list(collection.find({}, {'_id': 0}))
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
