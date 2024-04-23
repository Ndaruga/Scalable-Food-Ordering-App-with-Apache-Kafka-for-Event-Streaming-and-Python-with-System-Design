# Scalable Food Ordering App with Apache Kafka

This data engineering pipeline processes orders received from the customer frontend interface, calculates the total cost of orders, and sends confirmatory emails to customers. It goes ahead to visualize the orders being processed in real time with a dashboard.

Below is a short wideo of the dashboard analytics in realtime

https://github.com/Ndaruga/Scalable-Food-Ordering-App-with-Apache-Kafka-for-Event-Streaming-and-Python-with-System-Design/assets/68260816/0a243341-0ab2-44d8-b7b5-a17355865ca4



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

    * The cURL command in the `kafka-elasticsearch-connector.sh` file sends a POST request to Kafka Connect and creates the ElasticsearchSinkConnector named elasticsearch-sink. 
    
    * The Connector subscribes to the Kafka topic `Analysis-topic` and automatically creates a new `_doc` in ElasticSearch as soon as a new message is published to the topic `analysis-topic`. The name of the ElasticSearch index is the same as the name of the Kafka topic, i.e. Analysis-topic.key.ignore is set to true and means that Kafka message keys are not used as document IDs in ElasticSearch. Instead, the pattern `topic+partition+offset` is used to auto-generate the IDs.
    
    * Validate the creation of the Connector by running the following cURL command:
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


    * ElasticSearch: [http://localhost:9200](http://localhost:9200) to search/index documents in ElasticSearch (running in Docker) from your machine, [http://elastic:9200](http://elastic:9200) for communication between Docker services.
    * Kibana: [http://localhost:5601](http://localhost:5601) to have an easy way to access ElasticSearch via a GUI from your machine.

8. Configuring Kibana to Visualize Generated data
    > Please Note that these steps may vary but I will try to generalize them. The most crucial thing is creating an Index pattern
  -  Open elatic search on port [http://localhost:5601](http://localhost:5601).
  -  Select **Kibana**
  -  Select **Dashboard**, then select **New Dashboard** and then click on **Add data**
  -  Next you need to Click on `Create Index pattern` to create a pattern.

       * On Step 1 of 2: **Define an index pattern**, enter add the topic name defined in the elastic search connector set up which is `analysis_topic` and Click on **Next**

         <img width="1225" alt="image" src="https://github.com/Ndaruga/Scalable-Food-Ordering-App-with-Apache-Kafka-for-Event-Streaming-and-Python-with-System-Design/assets/68260816/26e135d3-01c5-4146-81f1-b25407baa0f2">
     
      * On Step 2 of 2: You can optionally give your index pattern a custom name under ***Advanced Settings*** or leave it as it is. Finally, click **Create Index Pattern**

  - Once the index pattern is created, Navigate to **Kibana** again and this time click **Create New Dashboard**
    
      <img width="587" alt="image" src="https://github.com/Ndaruga/Scalable-Food-Ordering-App-with-Apache-Kafka-for-Event-Streaming-and-Python-with-System-Design/assets/68260816/6e0f0d5e-16b1-4038-a752-8fe899ac8d2a">

  - Click on **Create New**
    
      <img width="301" alt="image" src="https://github.com/Ndaruga/Scalable-Food-Ordering-App-with-Apache-Kafka-for-Event-Streaming-and-Python-with-System-Design/assets/68260816/5c65467f-057c-4ed3-a5da-6cfda8393831">

  - In the `New Visualization` wizard, If you want to create a quick visual using drag and drop, select the `Lens` option. The **Lens** option, has limited customization unlike other options.
    
      <img width="416" alt="image" src="https://github.com/Ndaruga/Scalable-Food-Ordering-App-with-Apache-Kafka-for-Event-Streaming-and-Python-with-System-Design/assets/68260816/504d7462-6f6a-457e-9a06-f90ea6f2b5e6">

  - Next you can Drag your prefered fields from the right and drop them on the visual wizard in the center. Use the options on the Left to customize your aggregation.
    
      <img width="1495" alt="image" src="https://github.com/Ndaruga/Scalable-Food-Ordering-App-with-Apache-Kafka-for-Event-Streaming-and-Python-with-System-Design/assets/68260816/568dafce-5eb5-4728-8541-9ef292546de8">

      * You can select one of the suggested visuals on the panel below the main visual.
      * Click on **Save** to save your visual on the dashboard.
      * Add any other visuals that analysis data to the dashboard
    
  - Finally, Since the `recieved_orders.py` file generates orders after every 2 seconds, customize the time on the dashboard to `2 seconds` also set the refresh time to `2 seconds` and click **Start** then click on **Apply**
    
      <img width="525" alt="image" src="https://github.com/Ndaruga/Scalable-Food-Ordering-App-with-Apache-Kafka-for-Event-Streaming-and-Python-with-System-Design/assets/68260816/f235057e-d5cf-45ae-b492-60c0f9fe26b1">


### Congratulations!! You now have a Realtime Analytics Pipeline
---
## See Kafka Metrics, brokers and topics
* Kafka UI runs on [http://localhost:8080/](http://localhost:8080/)
  
  <img width="1510" alt="image" src="https://github.com/Ndaruga/Scalable-Food-Ordering-App-with-Apache-Kafka-for-Event-Streaming-and-Python-with-System-Design/assets/68260816/59a0edda-8b5b-4877-bfe2-26a4574840aa">

* Click on **topics** to see a list of all available Kafka topics as well as total messages published to these topics.
* Click on **consumers** to see the elasticsearch connector name we set up in step 5 of the setup.


## Additional Notes

- Mock orders are generated with random data using the `Faker` library.
- Confirmatory emails are sent to customers using their provided email addresses.
- Adjust the `ORDER_LIMIT` variable in `received_orders.py` to control the number of mock orders generated.

## License

This project is licensed under the [MIT License](LICENSE).

---
