# Install notes


kubectl logs -l serving.knative.dev/service=next-visit-test -c user-container -f --max-log-requests=100
