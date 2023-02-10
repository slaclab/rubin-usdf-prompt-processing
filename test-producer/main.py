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
    msg_batch_size = os.environ["MSG_BATCH_SIZE"]

    p = Producer(
        {"bootstrap.servers": kafka_cluster, "client.id": socket.gethostname()}
    )

    next_visit = {
        "instrument": "NotACam",
        "detector": 42,
        "salIndex": 1,
        "scriptSalIndex": 101,
        "groupId": "2023-01-23T23:33:14.762",
        "nimages": 2,
        "filters": "k1234",
        "coordinateSystem": 2,  # ICRS
        "position0": 0.0,
        "position1": 0.0,
        "rotationSystem": 2,    # Sky
        "cameraAngle": 0.0,
        "survey": "INVALID",
        "dome": 2,              # Open
        "duration": 35.0,
        "totalCheckpoints": 3,
    }

    for i in range(int(msg_batch_size)):
        p.produce(topic, json.dumps(next_visit).encode("utf-8"), callback=acked)

    p.poll(1)


if __name__ == "__main__":
    main()
