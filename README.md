# rubin-usdf-prompt-processing

This is the repository for the deployment of the prompt processing database, kafka cluster, and knative serving environment for the USDF.   It stores the kubernetes manifests, kubernetes operator configurations, and test Kafka producer and consumer code.  Deployments are done currently through make files.

See the [prompt prototype repo](https://github.com/lsst-dm/prompt_prototype) for the prompt prototype code.

To access the kuberentes environment login [here] (https://k8s.slac.stanford.edu/usdf-prompt-processing-dev) to obtain the kubernetes commmands to login and set your context.

Documentation on kafka, knative, and cnpg postgres is [here](docs)

## Local Development Links

If performing local deployments below are links to kubectl and kustomize.

[kubectl download](https://kubernetes.io/docs/tasks/tools/)
[Kustomize download](https://kubectl.docs.kubernetes.io/installation/kustomize/)