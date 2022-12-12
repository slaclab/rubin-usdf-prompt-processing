## Install notes

https://github.com/prometheus-community/helm-charts/tree/main/charts/kube-prometheus-stack

kubectl apply -f https://raw.githubusercontent.com/knative-sandbox/monitoring/main/servicemonitor.yaml
kubectl apply -f https://raw.githubusercontent.com/knative-sandbox/monitoring/main/grafana/dashboards.yaml

kubectl apply -f servicemonitor.yaml
