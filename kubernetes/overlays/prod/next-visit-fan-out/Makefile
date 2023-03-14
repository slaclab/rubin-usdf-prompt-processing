SECRET_PATH ?= secret/rubin/usdf-prompt-processing/next-visit-fan-out
BUTLER_SECRET_PATH ?= secret/rubin/usdf-butler/postgres
S3_SECRET_PATH ?= secret/rubin/usdf-prompt-processing/s3-buckets
DOCKER_SECRET_PATH ?= secret/rubin/usdf-prompt-processing/docker

get-secrets-from-vault:
	mkdir -p etc/.secrets/
	set -e; for i in kafka_pp_sasl_password kafka_pp_sasl_username; do vault kv get --field=$$i $(SECRET_PATH) > etc/.secrets/$$i ; done
	
	mkdir -p etc/.secrets/docker/
	set -e; for i in .dockerconfigjson; do vault kv get --field=$$i $(DOCKER_SECRET_PATH) > etc/.secrets/docker/$$i ; done

clean-secrets:
	rm -rf etc/.secrets/

run-kustomize:
	kubectl kustomize .

dump: get-secrets-from-vault run-kustomize clean-secrets

run-apply:
	kubectl apply -k .

apply: get-secrets-from-vault run-apply clean-secrets
