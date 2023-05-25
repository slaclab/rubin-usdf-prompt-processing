APDB_SECRET_PATH ?= secret/rubin/usdf-prompt-processing-dev/postgres
BUTLER_SECRET_PATH ?= secret/rubin/usdf-butler/postgres
S3_SECRET_PATH ?= secret/rubin/embargo/read/rubin-summit-users
CENTRAL_REPO_SECRET_PATH ?= secret/rubin/usdf-prompt-processing-dev/postgres
DOCKER_SECRET_PATH ?= secret/rubin/usdf-prompt-processing-dev/docker

get-secrets-from-vault:
	mkdir -p etc/.secrets/apdb
	set -e; for i in username password; do vault kv get --field=$$i $(APDB_SECRET_PATH) > etc/.secrets/apdb/$$i ; done
	
	mkdir -p etc/.secrets/butler/
	set -e; for i in username password; do vault kv get --field=$$i $(BUTLER_SECRET_PATH) > etc/.secrets/butler/$$i ; done

	mkdir -p etc/.secrets/s3/
	set -e; for i in access_key secret_key; do vault kv get --field=$$i $(S3_SECRET_PATH) > etc/.secrets/s3/$$i ; done

	mkdir -p etc/.secrets/central-repo/
	set -e; for i in central_repo_file; do vault kv get --field=$$i $(CENTRAL_REPO_SECRET_PATH) > etc/.secrets/central-repo/butler.yaml ; done

	mkdir -p etc/.secrets/docker/
	set -e; for i in .dockerconfigjson; do vault kv get --field=$$i $(DOCKER_SECRET_PATH) > etc/.secrets/docker/$$i ; done

run-kustomize:
	kubectl kustomize .

dump: get-secrets-from-vault run-kustomize clean-secrets

run-apply:
	kubectl apply -k .

apply: get-secrets-from-vault run-apply clean-secrets
