
SECRET_PATH ?= secret/rubin/usdf-prompt-processing-dev/postgres
BUTLER_SECRET_PATH ?= secret/rubin/usdf-butler/postgres
S3_SECRET_PATH ?= secret/rubin/usdf-prompt-processing-dev/s3-buckets
DOCKER_SECRET_PATH ?= secret/rubin/usdf-prompt-processing-dev/docker

get-secrets-from-vault:
	mkdir -p etc/.secrets/
	set -e; for i in username password; do vault kv get --field=$$i $(SECRET_PATH) > etc/.secrets/$$i ; done
	
	mkdir -p etc/.secrets/butler/
	set -e; for i in username password; do vault kv get --field=$$i $(BUTLER_SECRET_PATH) > etc/.secrets/butler/$$i ; done

	mkdir -p etc/.secrets/s3-buckets/
	set -e; for i in s3_credentials_ini_file bucket_url; do vault kv get --field=$$i $(S3_SECRET_PATH) > etc/.secrets/s3-buckets/$$i ; done

	mkdir -p etc/.secrets/docker/
	set -e; for i in .dockerconfigjson; do vault kv get --field=$$i $(DOCKER_SECRET_PATH) > etc/.secrets/docker/$$i ; done

clean-secrets:
	rm -rf etc/.secrets/
	rm -rf etc/.secretsbutler/

run-kustomize:
	kubectl kustomize .

dump: get-secrets-from-vault run-kustomize clean-secrets

run-apply:
	kubectl apply -k .

apply: get-secrets-from-vault run-apply clean-secrets
