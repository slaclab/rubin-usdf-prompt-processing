import logging
import json
import os
import sys
from confluent_kafka import Producer
import socket


def acked(err, msg):
    if err is not None:
        logging.error("Failed to deliver message: %s: %s", msg.value(), err)
    else:
        logging.info("Message produced: %s", msg.value())


def main():

    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

    # get kafka settings from env variables
    kafka_cluster = os.environ["KAFKA_CLUSTER"]
    topic = os.environ["BUCKET_NOTIFY_TOPIC"]

    p = Producer(
        {"bootstrap.servers": kafka_cluster, "client.id": socket.gethostname()}
    )

    next_visit = {
        "instrument": "NotACam",
        "detector": 42,
        "group": "visit-12882-20221027",
        "snaps": 2,
        "filter": "k1234",
        "ra": 0.0,
        "dec": 0.0,
        "rot": 0.0,
        "kind": "INVALID",
    }
    p.produce(topic, json.dumps(next_visit).encode("utf-8"), callback=acked)

    p.poll(1)


if __name__ == "__main__":
    main()
