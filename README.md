# Scalable Food Ordering App with Apache Kafka

This data engineering pipeline processes orders received from the customer frontend interface, calculates the total cost of orders, and sends confirmatory emails to customers. It goes ahead to visualize the orders being processed in real time with a dashboard.

Below is a short wideo of the dashboard analytics in realtime


The projects core component is [Apache Kafka](https://kafka.apache.org/) to stream evants (customer orders)

---
## System Design and Architecture
### Basic Architecure
![food-app drawio](https://github.com/Ndaruga/Scalable-Food-Ordering-App-with-Apache-Kafka-for-Event-Streaming-and-Python-with-System-Design/assets/68260816/b94cbd6f-2d82-4008-8dde-be4595e0d674)


### Data analysis Architecure

<img width="1346" alt="image" src="https://github.com/Ndaruga/Scalable-Food-Ordering-App-with-Apache-Kafka-for-Event-Streaming-and-Python-with-System-Design/assets/68260816/e86dbab7-a923-4405-adef-5f11710a8a64">


---

## Prerequisites

- [Docker](https://www.docker.com/products/docker-desktop/) and Docker Compose installed on your system.
   *  Before starting Docker, ensure to increase the memory allocation for containers to at least 6 GiB. The memory allocator can be found under the “Advanced” tab after opening the Docker Preferences.

      ![image](https://github.com/Ndaruga/Scalable-Food-Ordering-App-with-Apache-Kafka-for-Event-Streaming-and-Python-with-System-Design/assets/68260816/848083c3-a956-424b-872b-9136190b50b1)

- Python 3.x installed with necessary dependencies (see [requirements.txt](https://github.com/Ndaruga/Scalable-Food-Ordering-App-with-Apache-Kafka-for-Event-Streaming-and-Python-with-System-Design/blob/main/transactions.py)).

---

## Setup

1. Clone this repository to your local machine.

```bash
git clone https://github.com/Ndaruga/Scalable-Food-Ordering-App-with-Apache-Kafka-for-Event-Streaming-and-Python-with-System-Design.git
```

2. Install Python dependencies. 

```bash
pip install -r requirements.txt
```

3. Ensure that Kafka connected to elasticsearch

   * Make sure to create an empty folder in the same directory where the Docker compose file lives. `$PWD/connect-plugins` directs Kafka Connect to read the Java Connector files from this folder.

        ![image](https://github.com/Ndaruga/Scalable-Food-Ordering-App-with-Apache-Kafka-for-Event-Streaming-and-Python-with-System-Design/assets/68260816/c9712915-f550-43b1-8e8c-bc17fd3d77f2)

    * Connectors have the ability to handle Kafka message keys and values with different data formats. In this example, the message keys are expected to be a string and message values come in JSON format.

      Head over to the official Confluent website and download the Kafka-ElasticSearch Connector files: [https://www.confluent.io/hub/confluentinc/kafka-connect-elasticsearch](https://www.confluent.io/hub/confluentinc/kafka-connect-elasticsearch).

      ![image](https://github.com/Ndaruga/Scalable-Food-Ordering-App-with-Apache-Kafka-for-Event-Streaming-and-Python-with-System-Design/assets/68260816/c01d89c3-0234-4e62-9c21-dfe26340138c)

      Unzipp the downloaded ZIP file and move the entire uncompressed folder into the `connect-plugins` folder.


4. Start Docker with the following command:

    ```bash
    docker-compose up -d
    ```
    
    After a couple of minutes, you should see that all services started successfully.

5. Set up and activate the ElasticSearch-Kafka Connector by running the cURL command in your terminal:

    ```bash
    ./kafka-elasticsearch-connector.sh
    ```

    The cURL command in the `kafka-elasticsearch-connector.sh` file sends a POST request to Kafka Connect and creates the ElasticsearchSinkConnector named elasticsearch-sink. 
    
    The Connector subscribes to the Kafka topic `Analysis-topic` and automatically creates a new `_doc` in ElasticSearch as soon as a new message is published to the topic `analysis-topic`. The name of the ElasticSearch index is the same as the name of the Kafka topic, i.e. example-topic. key.ignore is set to true and means that Kafka message keys are not used as document IDs in ElasticSearch. 
    Instead, the pattern `topic+partition+offset` is used to auto-generate the IDs.
    
    Validate the creation of the Connector by running the following cURL command:
    ```
    curl -X GET http://localhost:8083/connectors
    ```
    This command should return the name of the connector
   <img width="648" alt="Screenshot 2024-04-23 at 12 46 01 PM" src="https://github.com/Ndaruga/Scalable-Food-Ordering-App-with-Apache-Kafka-for-Event-Streaming-and-Python-with-System-Design/assets/68260816/dccf9091-237a-4a4f-b16b-a435d9ceeef2">


7. Once all the Environments are set up, docker containers are up and running, you can now proceed to start generating your orders

    To ensure you see how your orders are being generated and processed, open 3 diffrent terminal windows on the project directory
     
    ![WhatsApp Image 2024-04-23 at 13 16 33](https://github.com/Ndaruga/Scalable-Food-Ordering-App-with-Apache-Kafka-for-Event-Streaming-and-Python-with-System-Design/assets/68260816/6302863c-82ff-4dc4-b050-c0e936c5fb49)

   Ensure you launch the python scrips as follows.
   
     - On terminal 3, run the `emails.py` script to listen for confirmed orders and send confirmatory emails to customers.
        ```bash
        python emails.py
        ```

     - On terminal 2, Run the `transactions.py` script to listen to incoming orders, process the orders by calculating the total costs, and publish the orders to the `confirmed_orders` Kafka topic.
        ```bash
        python transactions.py
        ```

     - On terminal 1, Run the `received_orders.py` script to pull from DB or/and generate mock orders and publish them to `recieved_orders` Kafka topic.

        ```bash
        python3 received_orders.py
        ```
    If all the file run successfully and simultaneously, you should see your orders being generated each after 2 seconds and processed simultanouesly as they are being generated.


    https://github.com/Ndaruga/Scalable-Food-Ordering-App-with-Apache-Kafka-for-Event-Streaming-and-Python-with-System-Design/assets/68260816/5c510c63-8145-42b0-a511-66b920f9939a


   The services are running on the following ports:
    
    * Kafka 7.2.0: [http://localhost:29092](http://localhost:29092) to connect to Kafka running in Docker from your machine,
      [http://broker:9092](http://broker:9092) used between Docker services inside the container.
    * Kafka Connect: [http://localhost:8083](http://localhost:8083) to setup and manage Connectors in Kafka Connect from your machine.
    * ElasticSearch: [http://localhost:9200](http://localhost:9200) to search/index documents in ElasticSearch (running in Docker) from your machine, [http://elastic:9200](http://elastic:9200) for communication between Docker services.
    * Kibana: [http://localhost:5601](http://localhost:5601) to have an easy way to access ElasticSearch via a GUI from your machine.

9. Configuring Kibana to Visualize Generated data





## Additional Notes

- Mock orders are generated with random data using the `Faker` library.
- Confirmatory emails are sent to customers using their provided email addresses.
- Adjust the `ORDER_LIMIT` variable in `received_orders.py` to control the number of mock orders generated.

## Dependencies

- `kafka-python`: Python client for Apache Kafka.
- `Faker`: Python library for generating fake data.

## Credits

- Original scripts developed by Ndaruga.

## License

This project is licensed under the [MIT License](LICENSE).

---
