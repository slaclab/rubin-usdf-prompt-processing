# Test Kafka Producer

This describes how to send test messages to trigger next visit.

To send messages test messages perform the following.

1.  Run `make run-apply` from this directory.  To edit the content of messages change the content or logic `p.produce` to send in different format of text to match the next visit json.  An output is generateds similar to below.  The timeis appended as a suffix to the job to make it unique.
```
kustomize edit set namesuffix "202210111003"
kubectl apply -k .
job.batch/nextvisit-producer-202210111003 created
```
2.  Run `kubectl logs job.batch/nextvisit-producer-202210111003 -n prompt-proto-service` to follow logs from the kafka producer.
```
INFO:root:Message produced: <cimpl.Message object at 0x7f475dcafa40>
```
3. Run `kubectl logs -l app=nextvisit-start -n prompt-proto-service -f` to follow logs for the kafka consumer and knative start deployment.  There will be similar output to below. 

```
INFO:root:Received message: {"message": "test"}
DEBUG:urllib3.connectionpool:Starting new HTTP connection (1): prompt-proto-service.prompt-proto-service.svc.cluster.local:80
DEBUG:urllib3.connectionpool:http://prompt-proto-service.prompt-proto-service.svc.cluster.local:80 "POST /next-visit HTTP/1.1" 502 73
```


## Producer Client
Producer documentation [here[(https://docs.confluent.io/kafka-clients/python/current/overview.html#ak-python)
