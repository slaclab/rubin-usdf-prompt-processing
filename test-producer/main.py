import logging
import json
import os
import sys
from confluent_kafka import Producer

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

# kafka
kafka_cluster = os.environ["KAFKA_CLUSTER"]
topic = os.environ["BUCKET_NOTIFY_TOPIC"]

# kafka auth
sasl_username = os.environ["SASL_USERNAME"]
sasl_password = os.environ["SASL_PASSWORD"]
sasl_mechanism = os.environ["SASL_MECHANISM"]
security_protoocol = os.environ["SECURITY_PROTOCOL"]


p = Producer(
    {
        "bootstrap.servers": kafka_cluster,
        "sasl.username": sasl_username,
        "sasl.password": sasl_password,
        "sasl.mechanism": sasl_mechanism,
        "security.protocol": security_protoocol,
    }
)

# p.produce(topic, "test1")
# p.produce(topic, "test2")
p.produce(topic, json.dumps({"message": "message 1"}))
p.produce(topic, json.dumps({"message": "message 2"}))
p.flush()
