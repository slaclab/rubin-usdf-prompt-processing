import logging
import json
import os
import sys
import socket
import logging
import asyncio
import typing
import httpx

import enum
from enum import Enum
import random

from aiokafka import AIOKafkaProducer
import dataclasses
from dataclasses import dataclass
from dataclasses_avroschema import AvroModel, types
from kafkit.registry.httpx import RegistryApi
from kafkit.registry import Serializer

# Logging config
logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.basicConfig(stream=sys.stderr, level=logging.WARNING)

kafka_cluster = os.environ["KAFKA_CLUSTER"]
topic = os.environ["BUCKET_NOTIFY_TOPIC"]
msg_batch_size = os.environ["MSG_BATCH_SIZE"]
kafka_schema_registry_url = os.environ["KAFKA_SCHEMA_REGISTRY_URL"]

# kafka auth
sasl_username = os.environ["SASL_USERNAME"]
sasl_password = os.environ["SASL_PASSWORD"]
sasl_mechanism = os.environ["SASL_MECHANISM"]
security_protocol = os.environ["SECURITY_PROTOCOL"]


class CoordSys(enum.IntEnum):
    # This is a redeclaration of lsst.ts.idl.enums.Script.MetadataCoordSys,
    # but we need Visit to work in code that can't import lsst.ts.
    NONE = 1
    ICRS = 2
    OBSERVED = 3
    MOUNT = 4


@dataclass
class NextVisitModel:

    coordsys = CoordSys

    class RotSys(enum.IntEnum):
        # Redeclaration of lsst.ts.idl.enums.Script.MetadataRotSys.
        NONE = 1
        SKY = 2
        HORIZON = 3
        MOUNT = 4

    class Dome(enum.IntEnum):
        # Redeclaration of lsst.ts.idl.enums.Script.MetadataDome.
        CLOSED = 1
        OPEN = 2
        EITHER = 3

    "Next Visit Message"
    private_efdStamp: int = "1674516757.7661333"
    private_kafkaStamp: int = "1674516794.7740011"
    salIndex: int
    private_revCode: str = "c9aab3df"
    private_sndStamp: int = "1674516794.7661333"
    private_rcvStamp: int = ""
    scriptSalIndex: int
    groupId: str
    nimages: int
    filters: str
    coordinateSystem: int
    # coordinateSystem: CoordSys = CoordSys.ICRS
    position: typing.List[int]
    rotationSystem: int
    cameraAngle: int
    survey: str
    dome: int
    duration: int
    totalCheckpoints: int


def acked(err, msg):
    if err is not None:
        logging.error("Failed to deliver message: %s: %s", msg.value(), err)
    else:
        logging.info("Message produced: %s", msg.value())


async def send(loop, total_events=3):
    producer = AIOKafkaProducer(
        loop=loop,
        bootstrap_servers=kafka_cluster,
        security_protocol=security_protocol,
        sasl_mechanism=sasl_mechanism,
        sasl_plain_username=sasl_username,
        sasl_plain_password=sasl_password,
    )
    # Get cluster layout and initial topic/partition leadership information
    await producer.start()

    schema = {
        "type": "record",
        "name": "logevent_nextVisit",
        "namespace": "lsst.sal.ScriptQueue",
        "fields": [
            {"name": "private_efdStamp", "type": "double"},
            {"name": "private_kafkaStamp", "type": "double"},
            {"name": "salIndex", "type": "long"},
            {"name": "private_revCode", "type": "string"},
            {"name": "private_sndStamp", "type": "double"},
            {"name": "private_rcvStamp", "type": "double"},
            {"name": "private_seqNum", "type": "long"},
            {"name": "private_identity", "type": "string"},
            {"name": "private_origin", "type": "long"},
            {"name": "scriptSalIndex", "type": "long"},
            {"name": "groupId", "type": "string"},
            {"name": "coordinateSystem", "type": "long"},
            {"name": "position", "type": {"type": "array", "items": "double"}},  # fix
            {"name": "cameraAngle", "type": "double"},
            {"name": "filters", "type": "string"},
            {"name": "dome", "type": "long"},
            {"name": "duration", "type": "double"},
            {"name": "nimages", "type": "long"},
            {"name": "survey", "type": "string"},
            {"name": "totalCheckpoints", "type": "long"},
        ],
    }

    async with httpx.AsyncClient() as client:
        registry_api = RegistryApi(http_client=client, url=kafka_schema_registry_url)
        serializer = await Serializer.register(registry=registry_api, schema=schema)

        for event_number in range(1, total_events + 1):
            # Produce message
            logging.info(f"Sending event number {event_number}")

            position_list = [0.0, 0.0]

            logging.info(CoordSys.ICRS.value)

            next_visit = NextVisitModel(
                salIndex=random.randint(1, 2),
                scriptSalIndex=random.randint(1, 2),
                groupId=random.choice(
                    [
                        "visit-12882-20221027",
                        "visit-12882-20221028",
                        "visit-12882-20221029",
                    ]
                ),
                nimages=random.randint(1, 3),
                filters=random.choice(["k1234", "k1235", "k1236"]),
                coordinateSystem=random.randint(1, 3),
                position=position_list,
                rotationSystem=random.randint(1, 3),
                cameraAngle=random.randint(1, 3),
                survey=random.choice(["k1234", "k1235", "k1236"]),
                dome=random.randint(1, 3),
                duration=random.randint(1, 3),
                totalCheckpoints=random.randint(1, 3),
            )

            print(next_visit)

            # create the message
            next_visit_message = await serializer(dataclasses.asdict(next_visit))

            await producer.send_and_wait(topic, next_visit_message)
            # sleep for 2 seconds
            await asyncio.sleep(2)
        else:
            # Wait for all pending messages to be delivered or expire.
            await producer.stop()
            logging.info("Stoping producer...")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    tasks = asyncio.gather(send(loop))

    loop.run_until_complete(tasks)
