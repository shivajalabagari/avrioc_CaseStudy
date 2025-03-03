from flask import Flask, render_template, jsonify
from pymongo import MongoClient

app = Flask(__name__)

# Connect to MongoDB
MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "user_data"
COLLECTION_NAME = "interactions"

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/data")
def get_data():
    data = list(collection.find({}, {"_id": 0}).limit(10))  # Get last 10 records
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
