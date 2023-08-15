SECRET_PATH ?= secret/rubin/usdf-prompt-processing/next-visit-fan-out

get-secrets-from-vault:
	mkdir -p etc/.secrets/
	set -e; for i in kafka_pp_sasl_password kafka_pp_sasl_username; do vault kv get --field=$$i $(SECRET_PATH) > etc/.secrets/$$i ; done

clean-secrets:
	rm -rf etc/.secrets/

run-kustomize:
	kubectl kustomize .

dump: get-secrets-from-vault run-kustomize clean-secrets

run-apply:
	kubectl apply -k .

apply: get-secrets-from-vault run-apply clean-secrets
