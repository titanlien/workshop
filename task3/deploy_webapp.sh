#!/bin/bash
set -e

# kustomize + kubectl appfy
kustomize build base/ | kubectl apply -f -

# wait pods is ready
sleep 5

# kubectl proxy
kubectl port-forward svc/webapp-2 8080:80 &
