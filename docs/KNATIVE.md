# Knative

Knative is an open source solution to be build serverless and event driven applications.  Overview [here](https://knative.dev/docs/serving/).  GCP CLoud Run is a managed instance of Knative Serving.

## Serving

Overview of serving [here](https://knative.dev/docs/serving/)

## Deploying a Knative service

Same application is [here](https://github.com/knative/docs/tree/main/code-samples/serving/hello-world/helloworld-python)

Below is an example Knative service.  Note the api version is `serving.knative.dev/v1`.  To create a service update the name, and environment variables under the container.

```
apiVersion: serving.knative.dev/v1
kind: Service
metadata:
  name: pp-test
spec:
  template:
    metadata:
      annotations:
        autoscaling.knative.dev/minScale: "1"
        autoscaling.knative.dev/maxScale: "10"
        autoscaling.knative.dev/target: "1"
    spec:
      imagePullSecrets:
      - name: regcred
      containers:
        - image: us-central1-docker.pkg.dev/prompt-proto/prompt/prompt-proto-service:latest
          env:
            - name: RUBIN_INSTRUMENT
              value: "lsst.obs.subaru.HyperSuprimeCam"
            - name: PUBSUB_VERIFICATION_TOKEN
              value: "rubin-prompt-proto-main"
            - name: IMAGE_BUCKET
              value: "rubin-prompt-proto-main"
            - name: CALIB_REPO
              value: "gs://rubin-prompt-proto-main/central_repo/butler-ip.yaml"
            - name: IP_APDB
              value: "10.109.19.42"
            - name: IP_REGISTRY
              value: "10.229.96.5:5432"
            - name: PSQL_REGISTRY_PASS
              valueFrom:
                secretKeyRef:
                  name: usdf-butler-creds
                  key: password
            - name: PSQL_APDB_PASS
              valueFrom:
                  secretKeyRef:
                    name: usdf-prompt-processing-creds
                    key: password
```

## Invoking Knative Service

The url is displayed after a Knative service is deployed and can also be obtained with `kubectl get route`

Knative Serving is deployed with Kourier as the ingress controller.  Knative Serving is not configured to be accessible outside of the Kubernetes and not for external DNS integration.  To invoke inside of the cluster a pod with curl ca be used `curl http://hello3.default.svc.cluster.local`.  Note the URL includes the namespace.

## Troubleshooting Services

To get a status of the service enter `kubectl get serving` with the appropriate namespace.  This shows the status of services, routes, configurations, and revisions.

Enter `kn services describe next-visit-start-test` to view the status of a service.  Note under the condiations that the services is ready with configurations and routes.  The same detail in a different format can be obtained with `kubectl describe ksvc next-visit-start-test`

```
Name:               next-visit-start-test
Namespace:          knative-eventing
Labels:             skaffold.dev/run-id=1c7c58d4-6b81-4e4b-981d-aa841844ed5a
Age:                1h
URL:                http://next-visit-start-test.knative-eventing.example.com
Image Pull Secret:  regcred

Revisions:  
  100%  @latest (next-visit-start-test-00001) [1] (1h)
        Image:     us-central1-docker.pkg.dev/prompt-proto/prompt/next-visit-test:31f9a67-dirty@sha256:0c42adc54b8dc94abc5337cdc61ee7cc3466fbbe85f9fab56e124d94f7413c57 (at 0c42ad)
        Replicas:  1/1

Conditions:  
  OK TYPE                   AGE REASON
  ++ Ready                   1h 
  ++ ConfigurationsReady     1h 
  ++ RoutesReady             1h 
```

### Logs

To get logs use the kubectl logs command.  Replace the name after`service=` with the name of the service. `kubectl logs -l serving.knative.dev/service=next-visit-start-test -c user-container`  Logs can also be viewed with kubectl logs and specifying the pod name.


## Eventing

Event sources are a link between an event producer and an event sink.  A sink can be a kubernetes service, knative service, channel, or a broker that receives events from an event source.  Full detail [here](https://knative.dev/docs/eventing/sources/)

To see available sources `kn source list -n knative eventing`

https://github.com/cloudevents/sdk-python

## Kafka Source

Log message for successful message to knative sunbscriber from kafka souce dispatcher.
```
{"@timestamp":"2022-10-21T15:52:34.695Z","@version":"1","message":"[Consumer clientId=consumer-knative-group-1, groupId=knative-group] Notifying assignor about the new Assignment(partitions=[next-visit-topic-0])","logger_name":"org.apache.kafka.clients.consumer.internals.ConsumerCoordinator","thread_name":"vert.x-kafka-consumer-thread-0","level":"INFO","level_value":20000}
{"@timestamp":"2022-10-21T15:52:34.695Z","@version":"1","message":"[Consumer clientId=consumer-knative-group-1, groupId=knative-group] Adding newly assigned partitions: next-visit-topic-0","logger_name":"org.apache.kafka.clients.consumer.internals.ConsumerCoordinator","thread_name":"vert.x-kafka-consumer-thread-0","level":"INFO","level_value":20000}
{"@timestamp":"2022-10-21T15:52:34.696Z","@version":"1","message":"[Consumer clientId=consumer-knative-group-1, groupId=knative-group] Setting offset for partition next-visit-topic-0 to the committed offset FetchPosition{offset=23, offsetEpoch=Optional.empty, currentLeader=LeaderAndEpoch{leader=Optional[prompt-processing-kafka-0.prompt-processing-kafka-brokers.kafka.svc:9092 (id: 0 rack: null)], epoch=0}}","logger_name":"org.apache.kafka.clients.consumer.internals.ConsumerCoordinator","thread_name":"vert.x-kafka-consumer-thread-0","level":"INFO","level_value":20000}
```

## Ceph Notification

Ceph S3 Notification compatability [here](https://docs.ceph.com/en/latest/radosgw/s3-notification-compatibility/)

Eventing Ceph configuration [here](https://github.com/knative-sandbox/eventing-ceph/tree/main/config)

## Remove stuck resources

Identify the stranded resources using this command.  Replace with the appropriate namespace. `kubectl api-resources --verbs=list --namespaced -o name | xargs -n 1 kubectl get --show-kind --ignore-not-found -n knative-serving`.  Reference link [here](https://stackoverflow.com/questions/52369247/namespace-stuck-as-terminating-how-i-removed-it)



## Get API Resources

```
kubectl api-resources --api-group='sources.knative.dev'
kubectl api-resources --api-group='messaging.knative.dev'
```