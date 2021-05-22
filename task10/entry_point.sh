#!/bin/bash

# init kubernetes environment
minikube start
minikube addons enable ingress
eval $(minikube docker-env --shell bash)

# bring up webapp service
docker build -t tree app/
kubectl apply -f k8s/webapp.yaml

echo "wait 7 seconds for pod become ready..."
sleep 7

# verify result
curl http://$(minikube ip)/tree -H Host:local.ecosia.org
