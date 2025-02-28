import json
from kafka import KafkaConsumer
from pymongo import MongoClient
from collections import defaultdict

consumer = KafkaConsumer(
    "user_interactions",
    bootstrap_servers="localhost:9092",
    auto_offset_reset="earliest",
    value_deserializer=lambda v: json.loads(v.decode('utf-8'))
)

mongo_client = MongoClient("mongodb://localhost:27017")
db = mongo_client["analytics"]
collection = db["aggregated_interactions"]

user_interactions = defaultdict(int)

for message in consumer:
    data = message.value
    user_interactions[data["user_id"]] += 1

    collection.update_one(
        {"metric": "user_avg"},
        {"$set": {"average_interactions": sum(user_interactions.values()) / len(user_interactions)}},
        upsert=True
    )

    print(f"Updated MongoDB: {user_interactions}")
