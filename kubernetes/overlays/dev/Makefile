KNATIVE_VERSION ?= v1.7.1
CNPG_VERSION ?= 1.17
CNPG_VERSION_MINOR ?= 0
SECRET_PATH ?= secret/rubin/usdf-prompt-processing-dev/postgres
BUTLER_SECRET_PATH ?= secret/rubin/usdf-butler/postgres

get-secrets-from-vault:
	mkdir -p etc/.secrets/
	set -e; for i in username password; do vault kv get --field=$$i $(SECRET_PATH) > etc/.secrets/$$i ; done
	
	mkdir -p etc/.secrets/butler/
	set -e; for i in username password; do vault kv get --field=$$i $(BUTLER_SECRET_PATH) > etc/.secrets/butler/$$i ; done

clean-secrets:
	rm -rf etc/.secrets/
	rm -rf etc/.secretsbutler/

update-cnpg-operator:
	curl -L https://raw.githubusercontent.com/cloudnative-pg/cloudnative-pg/release-$(CNPG_VERSION)/releases/cnpg-$(CNPG_VERSION).$(CNPG_VERSION_MINOR).yaml > cnpg-operator/cnpg-operator.yaml

update-knative-operator:
	curl -L https://github.com/knative/operator/releases/download/knative-$(KNATIVE_VERSION)/operator.yaml > knative-operator/knative-operator.yaml

run-kustomize:
	kubectl kustomize .

dump: get-secrets-from-vault run-kustomize clean-secrets

run-apply:
	kubectl apply -k .

apply: get-secrets-from-vault run-apply clean-secrets
