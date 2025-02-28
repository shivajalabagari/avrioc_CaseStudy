# avrioc_CaseStudy
CaseStudy

# **🚀 Kafka → MongoDB → CSV Data Pipeline in Gitpod**

This project sets up a **real-time data pipeline** using Kafka, MongoDB, and Flask for visualization. The steps below guide you through **starting, managing, and troubleshooting the pipeline in Gitpod**.

---

## **📌 Prerequisites**
Before running the pipeline, ensure:
- **Docker & Docker Compose** are installed in Gitpod.
- **Python Virtual Environment (`venv`)** is set up.
- **Kafka, MongoDB, and Zookeeper** are running correctly.

---

## **📌 Step 1: Set Up Gitpod and Environment**
### **🔹 Create a New Virtual Environment**
```bash
python -m venv venv
source venv/bin/activate
```

### **🔹 Install Dependencies**
```bash
pip install -r requirements.txt
```

---

## **📌 Step 2: Start Kafka, MongoDB, and Zookeeper**
Run the following command to **start all services**:
```bash
docker-compose up -d
```
✅ This starts **Kafka, Zookeeper, and MongoDB** in the background.

### **🔹 Verify Running Containers**
```bash
docker ps
```
✅ Expected output should list **Kafka, Zookeeper, and MongoDB**.

---

## **📌 Step 3: Run Kafka Producer (Data Generator)**
```bash
python data_generator.py
```
✅ Expected Output:
```plaintext
Produced: {'user_id': 12, 'item_id': 45, 'interaction_type': 'click', 'timestamp': '2025-02-28T12:34:56'}
```

---

## **📌 Step 4: Run Kafka Consumer (Store Data in MongoDB)**
```bash
python kafka_consumer.py
```
✅ Expected Output:
```plaintext
Updated MongoDB with user 12 interactions.
```

---

## **📌 Step 5: Verify Data in MongoDB**
### **🔹 Connect to MongoDB**
```bash
docker exec -it $(docker ps -qf "name=mongo") mongosh -u admin -p password --authenticationDatabase admin
```

### **🔹 Check Stored Data**
```javascript
use analytics
db.aggregated_interactions.find().pretty()
```
✅ Expected Output:
```json
{
  "metric": "user_avg",
  "average_interactions": 5.2
}
```

---

## **📌 Step 6: Export Data from MongoDB to CSV**
### **🔹 Export Data**
```bash
docker exec -it $(docker ps -qf "name=mongo") mongoexport --db analytics --collection aggregated_interactions --type=csv --fields metric,average_interactions --out /tmp/mongo_data.csv
```

### **🔹 Copy CSV File to Gitpod Workspace**
```bash
docker cp $(docker ps -qf "name=mongo"):/tmp/mongo_data.csv ./mongo_data.csv
```

### **🔹 Verify CSV Content**
```bash
cat mongo_data.csv
```
✅ **Now, `mongo_data.csv` should be ready for download!**

---

## **📌 Step 7: Download CSV and Open in Excel**
1. **Locate `mongo_data.csv` in Gitpod File Explorer.**
2. **Right-click → Download.**
3. **Open in Microsoft Excel.** 🎉

---

## **📌 Step 8: Start Flask API and View Dashboard**
```bash
python dashboard.py
```
✅ Open `http://localhost:5001/metrics` in your browser to view real-time data.

---

## **📌 Step 9: Open Multiple Terminals in Gitpod**
To manage different services efficiently:
- **New Terminal:** `Ctrl + Shift + ``
- **Split Terminal:** `Ctrl + Shift + 5`

✅ Example Setup:
| Terminal | Command |
|----------|---------|
| **Terminal 1** | `docker-compose up -d` |
| **Terminal 2** | `python data_generator.py` |
| **Terminal 3** | `python kafka_consumer.py` |
| **Terminal 4** | `python dashboard.py` |

---

## **🚀 Troubleshooting**
| Issue | Solution |
|-------|----------|
| `ModuleNotFoundError: No module named 'kafka'` | Run `pip install kafka-python` and retry. |
| MongoDB connection errors | Check credentials in `docker-compose.yml`. |
| No data in MongoDB | Ensure `data_generator.py` and `kafka_consumer.py` are running. |
| Empty CSV file | Verify `db.aggregated_interactions.find().pretty()` has data. |

---

## **🎯 Next Steps**
🔹 **Want to automate data exports?**
🔹 **Need real-time analytics in Google Sheets?**
Let me know how I can assist! 🚀🔥


# **🚀 Kafka → MongoDB → CSV Data Pipeline in Gitpod**

This project sets up a **real-time data pipeline** using Kafka, MongoDB, and Flask for visualization. The steps below guide you through **starting, managing, and troubleshooting the pipeline in Gitpod**.

---

## **📌 Prerequisites**
Before running the pipeline, ensure:
- **Docker & Docker Compose** are installed in Gitpod.
- **Python Virtual Environment (`venv`)** is set up.
- **Kafka, MongoDB, and Zookeeper** are running correctly.

---

## **📌 Step 1: Set Up Gitpod and Environment**
### **🔹 Create a New Virtual Environment**
```bash
python -m venv venv
source venv/bin/activate
```

### **🔹 Install Dependencies**
```bash
pip install -r requirements.txt
```

---

## **📌 Step 2: Set Up Kafka, MongoDB, and Zookeeper**
### **🔹 Create `docker-compose.yml`**
```yaml
version: "3.8"
services:
  zookeeper:
    image: confluentinc/cp-zookeeper:latest
    environment:
      ZOOKEEPER_CLIENT_PORT: 2181
    ports:
      - "2181:2181"

  kafka:
    image: confluentinc/cp-kafka:latest
    environment:
      KAFKA_BROKER_ID: 1
      KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://localhost:9092
    ports:
      - "9092:9092"

  mongodb:
    image: mongo:latest
    restart: always
    ports:
      - "27017:27017"
    environment:
      MONGO_INITDB_ROOT_USERNAME: admin
      MONGO_INITDB_ROOT_PASSWORD: password
    command: ["mongod", "--auth", "--setParameter", "enableLocalhostAuthBypass=false"]
    volumes:
      - mongodb_data:/data/db

volumes:
  mongodb_data:
```
### **🔹 Start Services**
```bash
docker-compose up -d
```
✅ This starts **Kafka, Zookeeper, and MongoDB** in the background.

### **🔹 Verify Running Containers**
```bash
docker ps
```
✅ Expected output should list **Kafka, Zookeeper, and MongoDB**.

---

## **📌 Step 3: Run Kafka Producer (Data Generator)**
### **🔹 Create `data_generator.py`**
```python
import json
import random
import time
from datetime import datetime
from kafka import KafkaProducer

KAFKA_BROKER = "localhost:9092"
KAFKA_TOPIC = "user_interactions"

producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

INTERACTION_TYPES = ["click", "view", "purchase"]

def generate_interaction():
    return {
        "user_id": random.randint(1, 1000),
        "item_id": random.randint(1, 500),
        "interaction_type": random.choice(INTERACTION_TYPES),
        "timestamp": datetime.now().isoformat()
    }

def produce_data(rate_per_sec=10):
    while True:
        interaction = generate_interaction()
        producer.send(KAFKA_TOPIC, value=interaction)
        print(f"Produced: {interaction}")
        time.sleep(1 / rate_per_sec)

if __name__ == "__main__":
    produce_data(rate_per_sec=50)
```
### **🔹 Run Producer**
```bash
python data_generator.py
```

---

## **📌 Step 4: Run Kafka Consumer (Store Data in MongoDB)**
### **🔹 Create `kafka_consumer.py`**
```python
import json
from kafka import KafkaConsumer
from pymongo import MongoClient

KAFKA_BROKER = "localhost:9092"
KAFKA_TOPIC = "user_interactions"
MONGO_URI = "mongodb://admin:password@localhost:27017/?authSource=admin"
MONGO_DB = "analytics"
MONGO_COLLECTION = "aggregated_interactions"

consumer = KafkaConsumer(
    KAFKA_TOPIC,
    bootstrap_servers=KAFKA_BROKER,
    auto_offset_reset="earliest",
    value_deserializer=lambda v: json.loads(v.decode("utf-8"))
)

mongo_client = MongoClient(MONGO_URI)
db = mongo_client[MONGO_DB]
collection = db[MONGO_COLLECTION]

for message in consumer:
    data = message.value
    collection.insert_one(data)
    print(f"Inserted: {data}")
```
### **🔹 Run Consumer**
```bash
python kafka_consumer.py
```

---

## **📌 Step 5: Verify and Export Data**
### **🔹 Verify Data in MongoDB**
```bash
docker exec -it $(docker ps -qf "name=mongo") mongosh -u admin -p password --authenticationDatabase admin
```
```javascript
use analytics
db.aggregated_interactions.find().pretty()
```
### **🔹 Export Data to CSV**
```bash
docker exec -it $(docker ps -qf "name=mongo") mongoexport --db analytics --collection aggregated_interactions --type=csv --fields metric,average_interactions --out /tmp/mongo_data.csv
docker cp $(docker ps -qf "name=mongo"):/tmp/mongo_data.csv ./mongo_data.csv
```

---

## **📌 Step 6: Start Flask API and View Dashboard**
### **🔹 Create `dashboard.py`**
```python
from flask import Flask, jsonify
from pymongo import MongoClient

app = Flask(__name__)

mongo_client = MongoClient("mongodb://admin:password@localhost:27017/?authSource=admin")
db = mongo_client["analytics"]
collection = db["aggregated_interactions"]

@app.route("/metrics", methods=["GET"])
def get_metrics():
    data = list(collection.find({}, {"_id": 0}))
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True, port=5001)
```


### **🔹 Run Flask API**
```bash
python dashboard.py
```
✅ Open `http://localhost:5001/metrics` to view real-time data.

---

## **📌 Step 7: Download CSV and Open in Excel**
1. **Locate `mongo_data.csv` in Gitpod File Explorer.**
2. **Right-click → Download.**
3. **Open in Microsoft Excel.** 🎉

