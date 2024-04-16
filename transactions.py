import json
from kafka import KafkaConsumer, KafkaProducer

RECIEVED_ORDER_KAFKA_TOPIC = "order_details"
CONFIRMED_ORDERS_KAFKA_TOPIC = "confirmed_orders"


consumer = KafkaConsumer(
    RECIEVED_ORDER_KAFKA_TOPIC,
    bootstrap_servers="localhost:29092"
)

producer = KafkaProducer(
    bootstrap_servers = "localhost:29092"
)

print(f"Listening for recieved orders...")
while True:
    for message in consumer:
        consumed_message = json.loads(message.value.decode())
        print(consumed_message)