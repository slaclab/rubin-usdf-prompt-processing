import json
import logging
import os
import sys
import asyncio
import httpx
import time

from aiokafka import AIOKafkaConsumer  # type:ignore
from cloudevents.conversion import to_structured
from cloudevents.http import CloudEvent
from dataclasses import dataclass
from pathlib import Path


def main():

    url = "https://usdf-rsp-dev.slac.stanford.edu/sasquatch-rest-proxy/topics/test.next-visit"
    header = {"Content-Type": "application/vnd.kafka.avro.v2+json"}
    header2 = {
        "Content-Type": "application/vnd.kafka.avro.v2+json",
        "Accept": "application/vnd.kafka.v2+json",
    }

    data = '{"value_schema_id": 1, "records": [{"value": {"private_efdStamp": 1674516757.7661333,"private_kafkaStamp": 1674516794.7740011,"salIndex": 2,"private_revCode": "c9aab3df","private_sndStamp": 1674516794.7661333,"private_rcvStamp": 1674516794.7662647,"private_seqNum": 22,"private_identity": "ScriptQueue:2","private_origin": 2786567,"scriptSalIndex": 200023,"groupId": "2023-01-23T23:33:14.762","coordinateSystem": 1,"position": [0,0],"rotationSystem": 1,"cameraAngle": 0,"filters": "","dome": 3,"duration": 2,"nimages": 0,"survey": "","totalCheckpoints": 0}}]}'

    r = httpx.post(url=url, headers=header, data=data)
    print(r.content)


if __name__ == "__main__":
    main()
