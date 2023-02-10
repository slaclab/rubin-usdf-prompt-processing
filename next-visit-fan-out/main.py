import json
import logging
import sys
import asyncio
import httpx
import yaml
from aiokafka import AIOKafkaConsumer
from cloudevents.conversion import to_structured
from cloudevents.http import CloudEvent
from pathlib import Path

import dataclasses
from dataclasses import dataclass
from dataclasses_avroschema import AvroModel


@dataclass
class NextVisitModel(AvroModel):
    "Next Visit Message"
    instrument: str
    group: str
    snaps: int
    filter: str
    ra: int
    dec: int
    rot: int
    kind: str

    @staticmethod
    def add_detectors(message, active_detectors):
        next_visit_message_dict = dataclasses.asdict(message)
        message_list = []
        for active_detector in active_detectors:
            temp_message = next_visit_message_dict.copy()
            temp_message["detector"] = active_detector
            message_list.append(temp_message)
        return message_list


def detector_load(conf, instrument):
    detectors = conf[instrument]["detectors"]
    active_detectors = []
    for key, value in detectors.items():
        if value in [True]:
            active_detectors.append(key)
    return active_detectors


async def main():

    # Get environment variables
    # kafka_cluster = os.environ["KAFKA_CLUSTER"]
    kafka_cluster = "34.123.148.90:9094"
    # group_id = os.environ["CONSUMER_GROUP"]
    group_id = "test-group-1"
    # topic = os.environ["BUCKET_NOTIFY_TOPIC"]
    topic = "next_visit_avro_topic"
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
        # value_deserializer=deserializer,
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
                    logging.info(
                        f"avro message value before deserialize is {msg.value}"
                    )
                    next_visit_message = NextVisitModel.deserialize(msg.value)
                    # next_visit_message_dict = dataclasses.asdict(next_visit_message)
                    logging.info(f"message deserialized {next_visit_message}")

                    match next_visit_message.instrument:
                        case "LATISS":
                            fan_out_message_list = next_visit_message.add_detectors(
                                next_visit_message, latiss_active_detectors
                            )
                        case "LSSTComCam":
                            fan_out_message_list = next_visit_message.add_detectors(
                                next_visit_message, lsst_com_cam_active_detectors
                            )
                        case "LSSTCam":
                            fan_out_message_list = next_visit_message.add_detectors(
                                next_visit_message, lsst_cam_active_detectors
                            )
                        case _:
                            raise Exception(
                                f"no matching case for {next_visit_message.instrument}"
                            )

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
