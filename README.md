# Scalable Food Ordering App with Apache Kafka

This data engineering pipeline processes orders received from the customer frontend interface, calculates the total cost of orders, and sends confirmatory emails to customers. 

It utilizes Apache Kafka for message streaming and communication between different components.

---
## System Design and Architecture
### Basic Architecure
![food-app drawio](https://github.com/Ndaruga/Scalable-Food-Ordering-App-with-Apache-Kafka-for-Event-Streaming-and-Python-with-System-Design/assets/68260816/b94cbd6f-2d82-4008-8dde-be4595e0d674)


### Data analysis Architecure

<img width="1346" alt="image" src="https://github.com/Ndaruga/Scalable-Food-Ordering-App-with-Apache-Kafka-for-Event-Streaming-and-Python-with-System-Design/assets/68260816/e86dbab7-a923-4405-adef-5f11710a8a64">


---
## Overview

The pipeline consists of three Python scripts:

1. **received_orders.py**: Generates mock orders and publishes them to the `received_orders` Kafka topic.
2. **transactions.py**: Consumes messages from the `received_orders` topic, calculates total order costs, and publishes confirmed orders to the `confirmed_orders` Kafka topic.
3. **emails.py**: Listens for confirmed orders from the `confirmed_orders` topic and sends confirmatory emails to customers.

## Prerequisites

- [Docker](https://www.docker.com/products/docker-desktop/) and Docker Compose installed on your system.
- Python 3.x installed with necessary dependencies (see `requirements.txt`).

## Setup

1. Clone this repository to your local machine.

```bash
git clone https://github.com/Ndaruga/Scalable-Food-Ordering-App-with-Apache-Kafka-for-Event-Streaming-and-Python-with-System-Design.git
```

2. Install Python dependencies.

```bash
pip install -r requirements.txt
```

3. Start Apache Kafka and other services using Docker Compose.

```bash
docker-compose up -d
```

## Usage
once all the docker containers are up and running, you can now proceed to start generating your orders

### 1. Generating Orders

Run the `received_orders.py` script to generate mock orders and publish them to `recieved_orders` Kafka topic.

```bash
python3 received_orders.py
```

### 2. Processing Orders

Run the `transactions.py` script to process orders, calculate total costs, and publish confirmed orders to the `confirmed_orders` Kafka topic.

```bash
python transactions.py
```

### 3. Sending Emails

Run the `emails.py` script to listen for confirmed orders and send confirmatory emails to customers.

```bash
python emails.py
```

## Configuration

- Kafka broker address: `localhost:29092`
- Kafka topics:
  - `received_orders`: Topic for receiving orders from the frontend.
  - `confirmed_orders`: Topic for confirmed orders after processing.

## Additional Notes

- Mock orders are generated with random data using the `Faker` library.
- Confirmatory emails are sent to customers using their provided email addresses.
- Adjust the `ORDER_LIMIT` variable in `received_orders.py` to control the number of mock orders generated.

## Dependencies

- `kafka-python`: Python client for Apache Kafka.
- `Faker`: Python library for generating fake data.

## Credits

- Original scripts developed by [Your Name].

## License

This project is licensed under the [MIT License](LICENSE).

---
