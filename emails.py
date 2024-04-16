import json

from kafka import KafkaConsumer

CONFIRMED_ORDERS_KAFKA_TOPIC = "confirmed_orders"

consumer = KafkaConsumer(
    CONFIRMED_ORDERS_KAFKA_TOPIC,
    bootstrap_servers="localhost:29092"
)

print("Waiting to send emails ...")
while True:
    for message in consumer:
        consumed_msg = json.loads(message.value.decode())
        mail = consumed_msg["Email"]
        print(f'Order ID {consumed_msg["order_id"]} sent to {consumed_msg["Customer_Name"].split(" ")[0]} via {mail}')