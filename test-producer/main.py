import logging
import json
import os
import sys
from confluent_kafka import Producer
import socket


def acked(err, msg):
    if err is not None:
        logging.error("Failed to deliver message: %s: %s" % (str(msg), str(err)))
    else:
        logging.info("Message produced: %s" % (str(msg)))


def main():

    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

    # get kafka settings from env variables
    kafka_cluster = os.environ["KAFKA_CLUSTER"]
    topic = os.environ["BUCKET_NOTIFY_TOPIC"]

    p = Producer(
        {"bootstrap.servers": kafka_cluster, "client.id": socket.gethostname()}
    )

    p.produce(topic, json.dumps({"message": "test"}), callback=acked)

    p.poll(1)


if __name__ == "__main__":
    main()
