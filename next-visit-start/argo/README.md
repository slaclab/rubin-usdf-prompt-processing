# Argo Events and Workflows

## Workflows

roles
https://github.com/argoproj/argo-workflows/blob/master/docs/managed-namespace.md

kubectl create namespace argo

kubectl create namespace argo
kubectl apply -n argo -f https://github.com/argoproj/argo-workflows/releases/download/v3.4.3/install.yaml


https://argoproj.github.io/argo-workflows/


kubectl patch deployment \
  argo-server \
  --namespace argo \
  --type='json' \
  -p='[{"op": "replace", "path": "/spec/template/spec/containers/0/args", "value": [
  "server",
  "--auth-mode=server"
]}]'


kubectl apply -n argo -f https://raw.githubusercontent.com/argoproj/argo-workflows/stable/manifests/install.yaml

wget https://raw.githubusercontent.com/argoproj/argo-workflows/master/examples/hello-world.yaml

argo submit -n argo --watch https://raw.githubusercontent.com/argoproj/argo-workflows/master/examples/hello-world.yaml

argo submit -n argo --watch hello-world.yaml

argo list -n argo
argo get -n argo @latest
argo logs -n argo @latest

https://quay.io/repository/argoproj/argo-eventbus


## Events

https://argoproj.github.io/argo-events/installation/

https://github.com/argoproj/argo-events/blob/master/api/event-source.md#kafkaeventsource

https://argoproj.github.io/argo-events/quick_start/

kubectl apply -n argo-events -f https://raw.githubusercontent.com/argoproj/argo-events/stable/examples/eventbus/native.yaml

# Event Bus

https://blog.argoproj.io/argo-events-v1-7-theres-a-new-bus-in-town-21949e915771

[config options](https://github.com/argoproj/argo-events/blob/master/api/event-bus.md#argoproj.io/v1alpha1.JetstreamBus)


kubectl create namespace argo-events

kubectl apply -f https://raw.githubusercontent.com/argoproj/argo-events/stable/manifests/install.yaml
# Install with a validating admission controller
kubectl apply -f https://raw.githubusercontent.com/argoproj/argo-events/stable/manifests/install-validating-webhook.yaml


helm repo add argo https://argoproj.github.io/argo-helm
helm install argo-events argo/argo-events


{"jetstream":{"url":"nats://eventbus-default-js-svc.argo-events.svc.cluster.local:4222","accessSecret":{"name":"eventbus-default-js-client-auth","key":"client-auth"},"streamConfig":"duplicates: 300s\nmaxage: 168h\nmaxbytes: -1\nmaxmsgs: 50000\nreplicas: 3\n"}}

{"jetstream":{"url":"nats://eventbus-default-js-svc.argo-events.svc.cluster.local:4222","accessSecret":{"name":"eventbus-default-js-client-auth","key":"client-auth"},"streamConfig":"duplicates: 300s\nmaxage: 168h\nmaxbytes: -1\nmaxmsgs: 50000\nreplicas: 3\n"}}

msg=eventBusConfig: {NATS:nil JetStream:&JetStreamConfig{
URL:nats://eventbus-default-js-svc.argo-events.svc.cluster.local:4222,AccessSecret:&v1.SecretKeySelector{LocalObjectReference:LocalObjectRefer
ence{Name:eventbus-default-js-client-auth,},Key:client-auth,Optional:nil,},StreamConfig:duplicates: 300s


