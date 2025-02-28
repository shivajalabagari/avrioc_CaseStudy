import json
import random
import time
from kafka import KafkaProducer
from datetime import datetime

producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def generate_event():
    return {
        "user_id": random.randint(1, 1000),
        "item_id": random.randint(1, 500),
        "interaction_type": random.choice(["click", "view", "purchase"]),
        "timestamp": datetime.now().isoformat()
    }

while True:
    event = generate_event()
    producer.send("user_interactions", value=event)
    print(f"Produced: {event}")
    time.sleep(0.5)
