import json
import logging
import sys
import asyncio
import httpx
import yaml
from aiokafka import AIOKafkaConsumer
from cloudevents.conversion import to_binary, to_structured
from cloudevents.http import CloudEvent
from pathlib import Path


def add_detectors_to_messages(message, active_detectors):
    message_list = []
    for active_detector in active_detectors:
        temp_message = message.copy()
        temp_message["detector"] = active_detector
        message_list.append(temp_message)
    return message_list


def deserializer(serialized):
    return json.loads(serialized)


def detector_load(conf, instrument):
    detectors = conf[instrument]["detectors"]
    active_detectors = []
    for key, value in detectors.items():
        if value in [True]:
            active_detectors.append(key)
    return active_detectors


async def main():

    # Get environment varialbles
    # kafka_cluster = os.environ["KAFKA_CLUSTER"]
    kafka_cluster = "34.123.148.90:9094"
    # group_id = os.environ["CONSUMER_GROUP"]
    group_id = "test-group-2"
    # topic = os.environ["BUCKET_NOTIFY_TOPIC"]
    topic = "next_visit_topic_2"
    # knative_serving_url = os.environ["KNATIVE_SERVING_URL"]
    knative_serving_url = (
        "http://next-visit-test.knative-serving.svc.cluster.local/next-visit"
    )

    # Logging config
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    logging.basicConfig(stream=sys.stderr, level=logging.WARNING)

    conf = yaml.safe_load(Path("detector.yaml").read_text())

    # list based on keys in config.  Data class
    latiss_active_detectors = detector_load(conf, "LATISS")
    lsst_com_cam_active_detectors = detector_load(conf, "LSSTComCam")
    lsst_cam_active_detectors = detector_load(conf, "LSSTCam")

    # kafka consumer setup
    consumer = AIOKafkaConsumer(
        topic,
        bootstrap_servers=kafka_cluster,
        group_id=group_id,
        value_deserializer=deserializer,
    )

    await consumer.start()

    tasks = set()

    async with httpx.AsyncClient() as client:
        try:
            while True:  # run continously
                async for msg in consumer:
                    logging.info(
                        f"Message value is {msg.value} at time ${msg.timestamp}"
                    )
                    logging.info(msg.value)

                    # hashmap name of instrument to detector variable
                    match msg.value["instrument"]:
                        case "LATISS":
                            fan_out_message_list = add_detectors_to_messages(
                                msg.value, latiss_active_detectors
                            )
                        case "LSSTComCam":
                            fan_out_message_list = add_detectors_to_messages(
                                msg.value, lsst_com_cam_active_detectors
                            )
                        case "LSSTCan":
                            fan_out_message_list = add_detectors_to_messages(
                                msg.value, lsst_cam_active_detectors
                            )
                        case _:
                            logging.info("no matching instrument")

                    try:
                        attributes = {
                            "type": "com.example.kafka",
                            "source": topic,
                        }

                        for fan_out_message in fan_out_message_list:
                            data = fan_out_message
                            data_json = json.dumps(data)

                            print(f"data after dump ${data_json}")
                            event = CloudEvent(attributes, data_json)
                            headers, body = to_structured(event)

                            task = asyncio.create_task(
                                client.post(
                                    knative_serving_url,
                                    headers=headers,
                                    data=body,
                                    timeout=None,
                                ),
                            )

                            tasks.add(task)
                            task.add_done_callback(tasks.discard)

                    except ValueError as e:
                        logging.info("Error ", e)

        finally:
            await consumer.stop()


asyncio.run(main())
