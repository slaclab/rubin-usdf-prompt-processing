DATE ?= $(shell date +%Y%m%d%H%M%S)

run-kustomize:
	kustomize edit set namesuffix "$(DATE)"
	kubectl kustomize .

run-apply:
	kustomize edit set namesuffix "$(DATE)"
	kubectl apply -k .
