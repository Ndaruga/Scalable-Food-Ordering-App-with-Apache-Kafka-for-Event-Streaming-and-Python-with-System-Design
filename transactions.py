'''
This File will:
    * Consume the messages sent to the recieved_orders topic.
    * Compute the total cost of the order.
    * Write (publish) the new transactional data (messages) into another confirmed_orders topic

'''


import json
from kafka import KafkaConsumer, KafkaProducer

RECIEVED_ORDER_KAFKA_TOPIC = "recieved_orders"
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

        # Send data to the confirmed orders topic

        data = {
            "purchase_date": consumed_message["date"],
            "order_id": consumed_message["order_id"],
            "Customer_Name": consumed_message["customer_name"],
            "Email": consumed_message["email"],
            "item": consumed_message["order_item"],
            "quantity": consumed_message["order_quantity"],
            "total_cost":consumed_message["order_quantity"] * consumed_message["cost"]
        }

        producer.send(
            CONFIRMED_ORDERS_KAFKA_TOPIC,
            json.dumps(data, indent=4, sort_keys=True, default=str).encode("utf-8")
        )

        # print(f'\nSent order ID: {consumed_message["order_id"]}')