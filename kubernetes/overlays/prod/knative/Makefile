
run-apply:
	kubectl apply -k .

apply: run-apply


patch-ingress:
  kubectl patch configmap/config-network \
    --namespace knative-serving \
    --type merge \
    --patch '{"data":{"ingress-class":"kourier.ingress.networking.knative.dev"}}'


