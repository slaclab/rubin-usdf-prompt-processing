import json
import logging
import os
import sys
import asyncio
import httpx
import yaml
import typing
import dataclasses
from aiokafka import AIOKafkaConsumer
from cloudevents.conversion import to_structured
from cloudevents.http import CloudEvent
from pathlib import Path
from dataclasses import dataclass
from kafkit.registry.httpx import RegistryApi
from kafkit.registry import Deserializer


@dataclass
class NextVisitModel:
    "Next Visit Message"
    salIndex: int
    scriptSalIndex: int
    groupId: str
    coordinateSystem: int
    position: typing.List[int]
    rotationSystem: int
    cameraAngle: float
    filters: str
    dome: int
    duration: float
    nimages: int
    survey: str
    totalCheckpoints: int

    def add_detectors(self, instrument, message, active_detectors):
        next_visit_message_dict = dataclasses.asdict(message)
        message_list = []
        for active_detector in active_detectors:
            temp_message = next_visit_message_dict.copy()
            temp_message["instrument"] = instrument
            temp_message["detector"] = active_detector
            # temporary change to modify blank filters to format expected by butler
            if temp_message["filters"] != "":
                temp_message["filters"] = (
                    "SDSS" + temp_message["filters"] + "_65mm~empty"
                )
            message_list.append(temp_message)
        return message_list


def detector_load(conf, instrument):
    detectors = conf[instrument]["detectors"]
    active_detectors = []
    for k, v in detectors.items():
        if v:
            active_detectors.append(k)
    return active_detectors


async def main():

    # Get environment variables
    detector_config_file = os.environ["DETECTOR_CONFIG_FILE"]
    kafka_cluster = os.environ["KAFKA_CLUSTER"]
    group_id = os.environ["CONSUMER_GROUP"]
    topic = os.environ["NEXT_VISIT_TOPIC"]
    kafka_schema_registry_url = os.environ["KAFKA_SCHEMA_REGISTRY_URL"]
    knative_serving_url = os.environ["KNATIVE_SERVING_URL"]
    offset = os.environ["OFFSET"]

    # kafka auth
    sasl_username = os.environ["SASL_USERNAME"]
    sasl_password = os.environ["SASL_PASSWORD"]
    sasl_mechanism = os.environ["SASL_MECHANISM"]
    security_protocol = os.environ["SECURITY_PROTOCOL"]

    # Logging config
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    logging.basicConfig(stream=sys.stderr, level=logging.WARNING)

    conf = yaml.safe_load(Path(detector_config_file).read_text())

    # list based on keys in config.  Data class
    latiss_active_detectors = detector_load(conf, "LATISS")
    lsst_com_cam_active_detectors = detector_load(conf, "LSSTComCam")
    lsst_cam_active_detectors = detector_load(conf, "LSSTCam")

    # kafka consumer setup
    consumer = AIOKafkaConsumer(
        topic,
        bootstrap_servers=kafka_cluster,
        group_id=group_id,
        security_protocol=security_protocol,
        sasl_mechanism=sasl_mechanism,
        sasl_plain_username=sasl_username,
        sasl_plain_password=sasl_password,
        auto_offset_reset=offset,
    )

    await consumer.start()

    tasks = set()

    async with httpx.AsyncClient() as client:

        try:
            # Setup kafka schema registry connection and deserialzer
            registry_api = RegistryApi(
                http_client=client, url=kafka_schema_registry_url
            )
            deserializer = Deserializer(registry=registry_api)

            while True:  # run continously
                async for msg in consumer:
                    logging.info(
                        f"Message value is {msg.value} at time ${msg.timestamp}"
                    )
                    logging.info(
                        f"avro message value before deserialize is {msg.value}"
                    )
                    next_visit_message_initial = await deserializer.deserialize(
                        data=msg.value
                    )

                    logging.info(f"message deserialized {next_visit_message_initial}")

                    next_visit_message_updated = NextVisitModel(
                        salIndex=next_visit_message_initial["message"]["salIndex"],
                        scriptSalIndex=next_visit_message_initial["message"][
                            "scriptSalIndex"
                        ],
                        groupId=next_visit_message_initial["message"]["groupId"],
                        coordinateSystem=next_visit_message_initial["message"][
                            "coordinateSystem"
                        ],
                        position=next_visit_message_initial["message"]["position"],
                        rotationSystem=next_visit_message_initial["message"][
                            "rotationSystem"
                        ],
                        cameraAngle=next_visit_message_initial["message"][
                            "cameraAngle"
                        ],
                        filters=next_visit_message_initial["message"]["filters"],
                        dome=next_visit_message_initial["message"]["dome"],
                        duration=next_visit_message_initial["message"]["duration"],
                        nimages=next_visit_message_initial["message"]["nimages"],
                        survey=next_visit_message_initial["message"]["survey"],
                        totalCheckpoints=next_visit_message_initial["message"][
                            "totalCheckpoints"
                        ],
                    )

                    match next_visit_message_updated.salIndex:
                        case 2:  # LATISS
                            fan_out_message_list = (
                                next_visit_message_updated.add_detectors(
                                    "LATISS",
                                    next_visit_message_updated,
                                    latiss_active_detectors,
                                )
                            )
                        # case "LSSTComCam":
                        #    fan_out_message_list = next_visit_message.add_detectors(
                        #        "LSSTComCam", next_visit_message, lsst_com_cam_active_detectors
                        #    )
                        case 1:  # LSSTCam
                            fan_out_message_list = (
                                next_visit_message_updated.add_detectors(
                                    "LSSTCam",
                                    next_visit_message_updated,
                                    lsst_cam_active_detectors,
                                )
                            )
                        case _:
                            raise Exception(
                                f"no matching case for salIndex {next_visit_message_updated.salIndex} to add instrument value"
                            )

                    try:
                        attributes = {
                            "type": "com.example.kafka",
                            "source": topic,
                        }

                        for fan_out_message in fan_out_message_list:
                            data = fan_out_message
                            data_json = json.dumps(data)

                            logging.info(f"data after json dump {data_json}")
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
