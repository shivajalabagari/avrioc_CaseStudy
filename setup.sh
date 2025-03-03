#!/bin/bash

echo "🚀 Setting up Kafka & MongoDB in Gitpod..."

# Install Kafka
if ! command -v kafka-server-start.sh &> /dev/null
then
  echo "Installing Kafka..."
  wget https://downloads.apache.org/kafka/3.5.0/kafka_2.13-3.5.0.tgz
  tar -xvzf kafka_2.13-3.5.0.tgz
  mv kafka_2.13-3.5.0 kafka
fi

# Install MongoDB
if ! command -v mongod &> /dev/null
then
  echo "Installing MongoDB..."
  sudo apt-get update
  sudo apt-get install -y mongodb
fi

# Start Services
echo "Starting MongoDB & Kafka..."
sudo service mongod start
sudo service kafka start

echo "✅ Setup Complete!"
