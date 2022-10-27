# Prompt Proto Knative Service

The knative serving instance is deployed in the prompt-proto-service namespace.

Deployments can be done via the makefile.  After updating a docker image update the image tag in the [prompt-proto-service-.yaml](prompt-proto-service.yaml) file in this directory.  Run `make apply` to deploy.  
If you are reusing a tag (e.g., for a branch build) and it refuses to deploy, update the revision field instead.

To obtain the service status `kubectl get serving -n prompt-proto-service`

## Knative Client

knative has client called `kn` that can be used to run simplified versions of commands to view, delete, and create services.  The `kn` client can be downloaded from [here](https://github.com/knative/client)

To see all services `kn service list -n prompt-proto-service`

To see if a service status `kn service describe prompt-proto-service -n prompt-proto-service`

Full user guide is [here](https://github.com/knative/client/blob/main/docs/README.md)

## Send test message

Run below to get an interactive terminal to send test mesages.  Replace with the appropriate topic.

```
kubectl -n kafka run kafka-producer -ti --image=strimzi/kafka:latest-kafka-2.4.0 --rm=true --restart=Never -- bin/kafka-console-producer.sh --broker-list prompt-processing-kafka-bootstrap:9092 --topic next-visit-test-topic
```

If there is error that producer already exists enter `kubectl delete pod kafka-producer-n kafka`
