#!/bin/bash

# Source the environment variables
source ./.env

# Use sourced variables in the cURL command
curl -X POST http://localhost:8083/connectors -H 'Content-Type: application/json' -d \
"{
  \"name\": \"$CONNECTOR_NAME\",
  \"config\": {
    \"connector.class\": \"io.confluent.connect.elasticsearch.ElasticsearchSinkConnector\",
    \"tasks.max\": \"1\",
    \"topics\": \"$ANALYSIS_KAFKA_TOPIC\",
    \"key.ignore\": \"true\",
    \"schema.ignore\": \"true\",
    \"connection.url\": \"http://elastic:9200\",
    \"type.name\": \"_doc\",
    \"name\": \"$CONNECTOR_NAME\",
    \"value.converter\": \"org.apache.kafka.connect.json.JsonConverter\",
    \"value.converter.schemas.enable\": \"false\"
  }
}"
