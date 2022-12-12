import json
import logging
import os
import sys
import asyncio
import httpx
from aiokafka import AIOKafkaConsumer
from cloudevents.conversion import to_binary, to_structured
from cloudevents.http import CloudEvent


def deserializer(serialized):
    return json.loads(serialized)


async def main():

    # Get environment varialbles
    kafka_cluster = os.environ["KAFKA_CLUSTER"]
    group_id = os.environ["CONSUMER_GROUP"]
    topic = os.environ["BUCKET_NOTIFY_TOPIC"]
    knative_serving_url = os.environ["KNATIVE_SERVING_URL"]

    # Logging config
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    logging.basicConfig(stream=sys.stderr, level=logging.WARNING)

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
                    logging.debug(
                        f"Message value is {msg.value} at time ${msg.timestamp}"
                    )

                    try:
                        attributes = {
                            "type": "com.example.kafka",
                            "source": topic,
                        }

                        data = msg.value
                        data_json = json.dumps(data)
                        event = CloudEvent(attributes, data_json)
                        headers, body = to_structured(event)

                        task = asyncio.create_task(
                            client.post(
                                knative_serving_url,
                                headers=headers,
                                data=body,
                                timeout=None,
                            )
                        )

                        tasks.add(task)
                        task.add_done_callback(tasks.discard)

                    except ValueError as e:
                        logging.info("Error ", e)

        finally:
            await consumer.stop()


asyncio.run(main())
