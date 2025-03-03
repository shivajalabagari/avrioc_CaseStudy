# dashboard/app.py
from flask import Flask, jsonify
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient('localhost', 27017)
db = client['interaction_metrics']

@app.route('/metrics', methods=['GET'])
def get_metrics():
    metrics = db.aggregations.find().sort("timestamp", -1).limit(1)
    return jsonify(metrics[0])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)