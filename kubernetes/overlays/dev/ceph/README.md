

## setup convenience aliases

```
❯ alias s3api="singularity exec /sdf/sw/s3/aws-cli_latest.sif aws --endpoint-url https://s3dfrgw.slac.stanford.edu s3api --profile=rubin-prompt-processing " 
❯ alias sns="singularity exec /sdf/sw/s3/aws-cli_latest.sif aws --endpoint-url https://s3dfrgw.slac.stanford.edu sns --profile=rubin-prompt-processing "
❯ alias s3="singularity exec /sdf/sw/s3/aws-cli_latest.sif aws --endpoint-url https://s3dfrgw.slac.stanford.edu s3 --profile=rubin-prompt-processing"
```

## setup user from vault creds

https://vault.slac.stanford.edu/ui/vault/secrets/secret/show/rubin/usdf-prompt-processing-dev/s3-buckets

```
❯ s3api configure
```

use `rubin-prompt-processing` as the profile name so it matches the above.



## make sure we can access the bucket

```
❯ s3api list-objects --bucket rubin-prompt-processing-test
``` 

## create topic endpoint for http

point the `push-endpoint` to the external bootstrap ip of the kafka server.

get the username and password with

```
❯ kg secrets yee-user -o jsonpath='{.data.sasl\.jaas\.config}' | base64 -d
```

get the ca cert with

```
❯ k get secrets yee-cluster-cluster-ca-cert -o jsonpath='{ .data.ca\.crt }' | base64 -d > yee-cluster.crt
```
```
❯ sns --region=default list-topics
❯ sns --region=default create-topic --name=rubin-prompt-processing-test  --attributes='{"push-endpoint": "kafka://user:password@172.24.5.223:9094", "use-ssl": "true", "ca-location": "yee-cluster.crt" }'
{
    "TopicArn": "arn:aws:sns:default:rubin:rubin-prompt-processing-test"
}
```

see https://docs.ceph.com/en/quincy/radosgw/notifications/

other useful commands

```
❯ sns --region=default delete-topic --topic-arn arn:aws:sns:default:rubin:rubin-prompt-processing-test
```

## validate the s3 topic

```
❯ sns --region=default list-topics
{
    "Topics": [
        {
            "TopicArn": "arn:aws:sns:default:rubin:rubin-prompt-processing-test"
        }
    ]
}
```

## configure the bucket notification

```
# configure the bucket notification
❯  s3api put-bucket-notification-configuration --bucket=rubin-prompt-processing-test --notification-configuration='{"TopicConfigurations": [{"Id": "rubin-prompt-processing-test", "TopicArn": "arn:aws:sns:default:rubin:rubin-prompt-processing-test", "Events": ["s3:ObjectCreated:*"]}]}'
```

## check bucket notifications

```
❯ s3api get-bucket-notification --bucket=rubin-prompt-processing-test
❯ s3api get-bucket-notification-configuration --bucket=rubin-prompt-processing-test
```



