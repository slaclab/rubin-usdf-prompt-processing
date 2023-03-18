# rubin-usdf-prompt-processing

This is the repository for the deployment of the prompt processing database, kafka cluster, and knative serving environment for the USDF.   It stores the kubernetes manifests, kubernetes operator configurations, and test Kafka producer and consumer code.  Deployments are done currently through make files.

See the [prompt prototype repo](https://github.com/lsst-dm/prompt_prototype) for the prompt prototype code.

To access the kuberentes environment login [here] (https://k8s.slac.stanford.edu/usdf-prompt-processing-dev) to obtain the kubernetes commmands to login and set your context.

Documentation on kafka, knative, and cnpg postgres is [here](docs)

## Local Development Links

If performing local deployments below are links to kubectl and kustomize.

[kubectl download](https://kubernetes.io/docs/tasks/tools/)
[Kustomize download](https://kubectl.docs.kubernetes.io/installation/kustomize/)

kubectl port-forward svc/prometheus-grafana 8080:80 -n prometheus

## View messages in topic

kubectl -n kafka run kafka-consumer -ti --image=quay.io/strimzi/kafka:0.33.2-kafka-3.4.0 --rm=true --restart=Never -- bin/kafka-console-consumer.sh --bootstrap-server prompt-processing-kafka-bootstrap:9092 --topic rubin-prompt-processing-prod --from-beginning