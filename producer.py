from kafka import KafkaProducer
import json
import time
import random

# Kafka Config
KAFKA_TOPIC = "user_interactions"
KAFKA_BROKER = "kafka:9092"

# Sample Data
users = ["Alice", "Bob", "Charlie", "David"]
actions = ["click", "view", "purchase", "logout"]

# Initialize Kafka Producer
producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

# Publish Messages to Kafka
while True:
    event = {
        "user": random.choice(users),
        "action": random.choice(actions),
        "timestamp": time.time()
    }
    producer.send(KAFKA_TOPIC, value=event)
    print(f"Produced: {event}")
    time.sleep(2)  # Simulate real-time events
