# Kafka

## Confluent Python Library
Link to github [here](https://github.com/confluentinc/confluent-kafka-python)


## Authentication

Confluent Python SASL Example [here](https://github.com/confluentinc/confluent-kafka-python/blob/master/examples/sasl_producer.py)

Example authentication kubernetes [here](https://github.com/strimzi/client-examples/blob/main/java/kafka/deployment-ssl-auth.yaml)

## Test Producer

```
kubectl -n kafka run kafka-producer -ti --image=strimzi/kafka:latest-kafka-2.4.0 --rm=true --restart=Never -- bin/kafka-console-producer.sh --broker-list prompt-processing-kafka-bootstrap:9092 --topic next-visit-test-topic
```

## Test Consumer

List Topics

```
kubectl -n kafka run kafka-topics -ti --image=strimzi/kafka:latest-kafka-2.4.0 --rm=true --restart=Never -- bin/kafka-topics.sh --list --bootstrap-server=prompt-processing-kafka-bootstrap:9092
```


### Kafkacat
Kafkacat can be installed with instructions [here](https://github.com/edenhill/kcat)

kafkacat commands to view topic.  `kafkacat -L -b 127.0.0.1:9092 -t my-topic`

List brokers and topics in the cluster.  `kafkacat -L -b 127.0.0.1:9092 -L`