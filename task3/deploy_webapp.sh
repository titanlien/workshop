#!/bin/bash
set -e

export webapp_tag=`git rev-parse --verify HEAD`

# update Menifests 
yasha --webapp_tag=$webapp_tag -v variables/common.yml -o web_1.yml --keep-trailing-newline \
  templates/web_1.yml.j2
exit 0

yasha -v variables/common.yml -o web_2.yml --keep-trailing-newline \
  templates/web_2.yml.j2

# kubectl appfy
kubectl apply -f web_1.yml -f web_2.yml

# wait pods is ready
sleep 5

# kubectl proxy
kubectl port-forward svc/webapp-2 8080:80 &
