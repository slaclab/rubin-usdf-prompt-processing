# Prompt Proto Knative Service

The knative serving instance is deployed in the prompt-proto-service namespace.

Deployments can be done via the makefile.  After updating a docker image update the image tag in the [prompt-proto-service-.yaml](prompt-proto-service.yaml) file in this directory.  Run `make apply` to deploy.  

To obtain the service status `kubectl get serving -n prompt-proto-service`