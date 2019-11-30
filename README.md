# workshop
# Task 1
## Terraform + AWS + Ansible
* create a new VPC with CIDR 172.16.0.0
* create two new subnets with CIDR 172.16.1.0/24 and 172.16.2.0/24 in two different availability zones
* create 5 new ec2 instances based on Ubuntu 18.04 (bionic)
* deploy the following Java application on these instances
* create a load balancer for the Java application on port 80
---
# Task 2
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
# Task 3
# docker + kubectl: deployment + svc
* Implement a piece of software exposing a JSON document:
```
{
“id”: “1”,
“message”: “Hello world” }
```
when visited with a HTTP client
* Dockerize the application
* Put the application to Minikube Kubernetes
* Create a second application, that utilizes the first and displays reversed message text
* Automate deployment of the 2 applications using a script