#!/bin/bash
set -e

export docker_hub_account=`cat variables/common.yml | yq .docker_hub_account -r`
export webapp_1_tag=`cat variables/common.yml | yq .webapp_1_tag -r`
export webapp_2_tag=`cat variables/common.yml | yq .webapp_2_tag -r`

# prepare docker webapp1 image
docker build -t $docker_hub_account/webapp1:$webapp_1_tag ./web1/
docker push $docker_hub_account/webapp1:$webapp_1_tag

# prepare docker webapp2 image
docker build -t $docker_hub_account/webapp2:$webapp_2_tag ./web2/
docker push $docker_hub_account/webapp2:$webapp_2_tag

# update Menifests 
yasha -v variables/common.yml -o web_1.yml --keep-trailing-newline \
  templates/web_1.yml.j2
yasha -v variables/common.yml -o web_2.yml --keep-trailing-newline \
  templates/web_2.yml.j2

# kubectl appfy
kubectl apply -f web_1.yml -f web_2.yml

# wait pods is ready
sleep 5

# kubectl proxy
kubectl port-forward svc/webapp-2 8080:80 &
