SECRET_PATH ?= secret/rubin/usdf-prompt-processing-dev/postgres
S3_SECRET_PATH ?= secret/rubin/usdf-prompt-processing-dev/s3-buckets

get-secrets-from-vault:
	mkdir -p etc/.secrets/
	set -e; for i in password username; do vault kv get --field=$$i $(SECRET_PATH) > etc/.secrets/$$i ; done
	set -e; for i in access_key secret_key; do vault kv get --field=$$i $(S3_SECRET_PATH) > etc/.secrets/$$i ; done

clean-secrets:
	rm -rf etc/.secrets/

run-kustomize:
	kubectl kustomize .

dump: get-secrets-from-vault run-kustomize clean-secrets

run-apply:
	kubectl apply -k .

apply: get-secrets-from-vault run-apply clean-secrets
