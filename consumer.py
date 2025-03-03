from kafka import KafkaConsumer
import json
from pymongo import MongoClient

# Kafka & MongoDB Config
KAFKA_TOPIC = "user_interactions"
KAFKA_BROKER = "localhost:9092"
MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "user_data"
COLLECTION_NAME = "interactions"

# Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

# Initialize Kafka Consumer
consumer = KafkaConsumer(
    KAFKA_TOPIC,
    bootstrap_servers=KAFKA_BROKER,
    value_deserializer=lambda x: json.loads(x.decode("utf-8"))
)

# Consume Messages and Store in MongoDB
for message in consumer:
    print(f"Consumed: {message.value}")
    collection.insert_one(message.value)
