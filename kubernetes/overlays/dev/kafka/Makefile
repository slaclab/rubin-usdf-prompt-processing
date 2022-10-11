
NAMESPACE ?= kafka

update-operator:
	curl -L "https://strimzi.io/install/latest?namespace=$(NAMESPACE)" > strimzi-operator.yaml

persistent-single:
	curl -L https://strimzi.io/examples/latest/kafka/kafka-persistent-single.yaml > kafka-persistent-single.yaml

producer:
	kubectl -n $(NAMESPACE) run kafka-producer -ti --image=quay.io/strimzi/kafka:0.31.1-kafka-3.2.3 --rm=true --restart=Never -- bin/kafka-console-producer.sh --bootstrap-server my-cluster-kafka-bootstrap:9092 --topic my-topic

receiver:
	kubectl -n $(NAMESPACE) run kafka-consumer -ti --image=quay.io/strimzi/kafka:0.31.1-kafka-3.2.3 --rm=true --restart=Never -- bin/kafka-console-consumer.sh --bootstrap-server my-cluster-kafka-bootstrap:9092 --topic my-topic --from-beginning

run-dump:
	kubectl kustomize .

dump: run-dump

run-apply:
	kubectl apply -k .

apply: run-apply


