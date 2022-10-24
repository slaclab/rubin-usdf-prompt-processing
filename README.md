# rubin-usdf-prompt-processing


## K8s

[K8s Dev link](https://k8s.slac.stanford.edu/usdf-prompt-processing-dev)


```
kubectl port-forward svc/my-cluster-kafka-bootstrap 9093:9093 -n kafka
```

## Kafka

Strimzi link [here](https://github.com/strimzi)

## Test Producer

```
kubectl -n kafka run kafka-producer -ti --image=strimzi/kafka:latest-kafka-2.4.0 --rm=true --restart=Never -- bin/kafka-console-producer.sh --broker-list prompt-processing-kafka-bootstrap:9092 --topic next-visit-test-topic
```

## Test Consumer

List Topics

```
kubectl -n kafka run kafka-topics -ti --image=strimzi/kafka:latest-kafka-2.4.0 --rm=true --restart=Never -- bin/kafka-topics.sh --list --bootstrap-server=prompt-processing-kafka-bootstrap:9092
```

## Confluent Python Library

[GitHub Repo](https://github.com/confluentinc/confluent-kafka-python)



