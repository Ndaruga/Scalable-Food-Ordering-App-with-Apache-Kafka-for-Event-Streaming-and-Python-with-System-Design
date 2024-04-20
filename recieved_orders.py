'''
This file will:
    * Recieve orders from the the customer frontend interface 
    * Publish them to the recieved_orders kafka topic
'''
import json
import time
import random
from faker import Faker
from datetime import datetime

from kafka import KafkaProducer

ORDER_KAFKA_TOPIC = "recieved_orders"
ORDER_LIMIT = 1500
fake = Faker()

producer = KafkaProducer(
    bootstrap_servers="localhost:29092"
)

print("Generating orders in random times ...")

for i in range(1, ORDER_LIMIT):
    data = {
        "date": datetime.now(),
        "order_id": i,
        "user_id": fake.uuid4(),
        "customer_name": fake.name(),
        "email": fake.email(),
        "order_item": fake.random_element(["Water Dispenser", "Microwave", "Laptop", "Monitor", "Cooker", "TV", "Router", "Fridge"]),
        "order_quantity": random.choice(range(1,4)),
        "cost": 200*random.choice(range(91, 115))
    }

    producer.send(
        ORDER_KAFKA_TOPIC,
        json.dumps(data, indent=4, sort_keys=True, default=str).encode("utf-8")
    )

    print(f"Done sending {i}")
    time.sleep(random.choice(range(1, 11)))

