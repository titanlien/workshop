# workshop
# [Task 1](task1)
## Terraform + AWS + Ansible
* create a new VPC with CIDR 172.16.0.0
* create two new subnets with CIDR 172.16.1.0/24 and 172.16.2.0/24 in two different availability zones
* create 5 new ec2 instances based on Ubuntu 18.04 (bionic)
* deploy the following Java application on these instances
* create a load balancer for the Java application on port 80
* setup route53 to host CNAME record of elb url
---
# [Task 2](task2)
## Nginx + docker-compose + python
* creates a new Docker container running nginx and proxies all requests on /<container_name> to the appropriate container and port
	* there is only one nginx container running at all times
	* if the nginx container is down, it needs to be started
	* when a new application container is created the nginx configuration is updated to proxy requests to the new container
* creates a new Docker container running Java and deploys demo-0.0.1-SNAPTSHOT.jar from the previous step
	* the Docker container publishes container 8080 on a free port between 8000 and 8200
	* the container name is a unique identifier
	* container is only created if it does not exist
	* there can be multiple Docker containers with different names running at the same time

---
# [Task 3](task3)
# github workflow + kustomize + kubectl: deployment + svc
* Implement a piece of software exposing a JSON document:
```
{
"id": "1",
"message": "Hello world"
}
```
when visited with a HTTP client
* Dockerize the application
* Put the application to kind's Kubernetes
* Create a second application, that utilizes the first and displays reversed message text
* Deployment docker image with github workflow and login github registry with k8s secret config.
* Update application with kubctl in script
---
# [Task 4](task4)
# Python CLI
* Please consider the work you submit here a small, but production-ready deliverable, in the sense that you are happy to ship such code, tests and documentation.
* Write a Roman numeral converter that converts integer numbers into Roman numerals:

```
func(36)

Output: "XXXVI"
```
---
# [Task 5](task5)
# Go tutorial on jupyter notebook
[html preview](https://htmlpreview.github.io/?https://github.com/titanlien/workshop/blob/master/task5/go_tuturial.html)

---
# [Task 6](task6)
## 6.1 Creare a ruby script
### It shows top 10 process in swap and sorts output by KB. It will ignore Zero values


## 6.2 Create a bach script

```
performs occasional test queries to the hostname "google.com" to each of the DNS servers configured in /etc/resolv.conf
```

## 6.3 Fix a client certificateds issue in nginx configure.


---
# [Task 7](task7)
### setup backend api to handle POST/PUT/PATCH and query value metadata by filtering metadata key

* Technical scopes

```
github action
docker-compose
pytest
fastapi
minikube
make
Using helm to provision mongodb
```

---
# [Task 8](task8)
### Istio 1.6.8 present canary deploy on minikube

---
# [Task 9](https://gitlab.com/maohsiang_lien/blue-green)
### CI/CD within helm bluegreen deploy and release tag on gitlab  pipelines
[Gitlab pipeline](https://gitlab.com/maohsiang_lien/blue-green)

---
# [Task 10](task10)
### build up a API to return GET request, and create a docker image on minikube, then create manifests to bring up the service and deployment.

---
# [Task 11](task11)

### This program is going to be provided ​json​ lines as input in the ​stdin​, and should provide a ​json​ line output for each one — imagine this as a stream of events arriving at the authorizer.
```
$ cat operations
{"account": {"active-card": true, "available-limit": 100}} {"transaction": {"merchant": "Burger King", "amount": 20, "time": "2019-02-13T10:00:00.000Z"}}
{"transaction": {"merchant": "Habbib's", "amount": 90, "time": "2019-02-13T11:00:00.000Z"}}
$ authorize < operations
{"account": {"active-card": true, "available-limit": 100}, "violations": []} {"account": {"active-card": true, "available-limit": 80}, "violations": []} {"account": {"active-card": true, "available-limit": 80}, "violations": ["insufficient-limit"]}
```
