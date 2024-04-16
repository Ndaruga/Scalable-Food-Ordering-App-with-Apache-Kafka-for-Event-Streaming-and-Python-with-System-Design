import json
import time
import random
from faker import Faker
from datetime import datetime

from kafka import KafkaProducer

ORDER_KAFKA_TOPIC = "order_details"
ORDER_LIMIT = 15
fake = Faker()

producer = KafkaProducer(
    bootstrap_servers="localhost:29092"
)

print("Generating orders in random times ...")

for i in range(1, ORDER_LIMIT):
    data = {
        "date": datetime.now(),
        "Order_id": i,
        "User_id": fake.uuid4(),
        "customer_name": fake.name(),
        "order_item": fake.random_element(["Water Dispenser", "Microwave", "Laptop", "Monitor", "Cooker", "TV", "Router", "Fridge"]),
        "order_quantity": random.choice(range(1,4)),
        "total_cost": 200*random.choice(range(100, 115))
    }

    producer.send(
        ORDER_KAFKA_TOPIC,
        json.dumps(data, indent=4, sort_keys=True, default=str).encode("utf-8")
    )

    print(f"Done sending {i}")
    time.sleep(3)

