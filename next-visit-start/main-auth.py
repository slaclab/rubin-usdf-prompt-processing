import logging
import os
import sys
from confluent_kafka import Consumer
import requests
import json
from requests import HTTPError


logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

# kafka
kafka_cluster = os.environ["KAFKA_CLUSTER"]
group_id = os.environ["CONSUMER_GROUP"]
topic = os.environ["BUCKET_NOTIFY_TOPIC"]

# kafka auth
sasl_username = os.environ["SASL_USERNAME"]
sasl_password = os.environ["SASL_PASSWORD"]
sasl_mechanism = os.environ["SASL_MECHANISM"]
security_protoocol = os.environ["SECURITY_PROTOCOL"]

# knative serving
knative_serving_url = os.environ["KNATIVE_SERVING_URL"]

c = Consumer(
    {
        "bootstrap.servers": kafka_cluster,
        "group.id": group_id,
        "auto.offset.reset": "earliest",
        "sasl.username": sasl_username,
        "sasl.password": sasl_password,
        "security.protocol": security_protoocol,
        "sasl.mechanism": sasl_mechanism,
    }
)

c.subscribe([topic])

try:
    while True:
        msg = c.poll(1.0)

        if msg is None:
            # logging.info("Msg is none")
            continue
        if msg.error():
            logging.info("Consumer error: {}".format(msg.error()))
            continue

        logging.info("Received message: {}".format(msg.value().decode("utf-8")))

        if msg:
            try:
                json_message = msg.value().decode("utf-8")
                response = requests.post(knative_serving_url, json=json_message)
                logging.info(response.status_code)
            except HTTPError as ex:
                logging.info("Exception ", ex)

finally:
    c.close()
