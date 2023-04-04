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

## Revisions

A knative revision is created for each deployment of the prompt proto service.  To see the current revision list enter `kubectl get revision -n prompt-proto-service` Enter `kubectl delete revision <revision name> -n prompt-proto-service` replace `<revision name>` with the appropriate revision name.

Prompt Prototype docker image builds currently use tags that match the branch number.  There can be more than 1 build that has the same tag.  Knative works on the concept of revisisions and that something changed between revision.  The `imagePullPolicy` on the prompt prototype service is set to always pull during development to force a download.  The `revision` annotation on [prompt-proto-service.yaml](prompt-proto-service.yaml) can also be incremented to force a new revision if one does not deploy because nothing changed in the service defintion to signal a new revision.  Please note when moving to production different image tags (for example a version number, git commit short SHA, or release) should be used to allow for revisions to be matched to the code deployed and for quicker rollback.