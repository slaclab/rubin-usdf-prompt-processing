# Kafka

## Confluent Python Library
Link to github [here](https://github.com/confluentinc/confluent-kafka-python)


## Authentication

Confluent Python SASL Example [here](https://github.com/confluentinc/confluent-kafka-python/blob/master/examples/sasl_producer.py)

Example authentication kubernetes [here](https://github.com/strimzi/client-examples/blob/main/java/kafka/deployment-ssl-auth.yaml)

## Testing

Create a message

```
kubectl -n kafka run kafka-producer -ti --image=strimzi/kafka:latest-kafka-2.4.0 --rm=true --restart=Never -- bin/kafka-console-producer.sh --broker-list my-cluster-kafka-bootstrap:9092 --topic my-topic`
```

Read a message
```
kubectl -n kafka run kafka-consumer -ti --image=strimzi/kafka:latest-kafka-2.4.0 --rm=true --restart=Never -- bin/kafka-console-consumer.sh --bootstrap-server my-cluster-kafka-bootstrap:9092 --topic my-topic --from-beginning
```

### Kafkacat
Kafkacat can be installed with instructions [here](https://github.com/edenhill/kcat)

kafkacat commands to view topic.  `kafkacat -L -b 127.0.0.1:9092 -t my-topic`

List brokers and topics in the cluster.  `kafkacat -L -b 127.0.0.1:9092 -L`