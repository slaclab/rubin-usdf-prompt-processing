VERSION ?= v1.7.1


#knative-yaml:
#	curl -L https://github.com/knative/eventing/releases/download/knative-$(VERSION)/eventing-crds.yaml > eventing-crds.yaml
#	curl -L https://github.com/knative/eventing/releases/download/knative-$(VERSION)/eventing-core.yaml > eventing-core.yaml
#	curl -L https://github.com/knative-sandbox/eventing-kafka-broker/releases/download/knative-v1.7.2/eventing-kafka-controller.yaml > eventing-kafka-controller.yaml
#	curl -L https://github.com/knative-sandbox/eventing-kafka-broker/releases/download/knative-v1.7.2/eventing-kafka-channel.yaml > eventing-kafka-channel.yaml
#	curl -L https://github.com/knative-sandbox/eventing-kafka-broker/releases/download/knative-v1.7.2/eventing-kafka-broker.yaml > eventing-kafka-broker.yaml
#	curl -L https://github.com/knative-sandbox/eventing-kafka-broker/releases/download/knative-v1.7.2/eventing-kafka-sink.yaml > eventing-kafka-sink.yaml
#
#apply-knative-yaml:
#	kubectl apply -f eventing-crds.yaml -f eventing-core.yaml -f eventing-kafka-controller.yaml -f eventing-kafka-channel.yaml -f eventing-kafka-broker.yaml -f eventing-kafka-sink.yaml

update-operator:
	curl -L https://github.com/knative/operator/releases/download/knative-v1.7.1/operator.yaml > knative-operator/knative-operator.yaml

dump:
	kubectl kustomize .

run-apply:
	kubectl apply -k .

apply: run-apply
