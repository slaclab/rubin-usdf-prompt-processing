
KAFKA_NAMESPACE ?= kafka

SINGULARITY_IMAGE ?= kafka_0.31.1-kafka-3.2.3.sif

BOOTSTRAP_SERVER ?= prompt-processing-kafka-bootstrap:9092

SECRET_PATH ?= secret/rubin/usdf-prompt-processing-dev/postgres
BUTLER_SECRET_PATH ?= secret/rubin/usdf-butler/postgres
S3_SECRET_PATH ?= secret/rubin/embargo/read/rubin-summit-users
DOCKER_SECRET_PATH ?= secret/rubin/usdf-prompt-processing/docker

get-secrets-from-vault:
	mkdir -p etc/.secrets/
	set -e; for i in username password; do vault kv get --field=$$i $(SECRET_PATH) > etc/.secrets/$$i ; done

	mkdir -p etc/.secrets/butler/
	set -e; for i in username password; do vault kv get --field=$$i $(BUTLER_SECRET_PATH) > etc/.secrets/butler/$$i ; done

	mkdir -p etc/.secrets/s3/
	set -e; for i in access_key secret_key; do vault kv get --field=$$i $(S3_SECRET_PATH) > etc/.secrets/s3/$$i ; done

	mkdir -p etc/.secrets/docker/
	set -e; for i in .dockerconfigjson; do vault kv get --field=$$i $(DOCKER_SECRET_PATH) > etc/.secrets/docker/$$i ; done

clean-secrets:
	rm -rf etc/.secrets/

create-singularity:
	singularity pull -F docker://quay.io/strimzi/kafka:0.31.1-kafka-3.2.3

producer: 
	singularity exec $(SINGULARITY_IMAGE) /opt/kafka/bin/kafka-console-producer.sh --bootstrap-server $(BOOTSTRAP_SERVER) --topic $(KAFKA_TOPIC)

run-kustomize:
	kubectl kustomize .

dump: get-secrets-from-vault run-kustomize clean-secrets

run-apply:
	kubectl apply -k .

apply: get-secrets-from-vault run-apply clean-secrets
