![Mao-Hsiang's GitHub stats](https://github-readme-stats.vercel.app/api?username=titanlien&show_icons=true&theme=ocean_dark)

[![Top Langs](https://github-readme-stats.vercel.app/api/top-langs/?username=titanlien&hide=c,perl,html,java,objective-c,css&theme=ocean_dark)](https://github.com/anuraghazra/github-readme-stats)
# workshop
# [Task 1](task01)
## Terraform + AWS + Ansible
* create a new VPC with CIDR 172.16.0.0
* create two new subnets with CIDR 172.16.1.0/24 and 172.16.2.0/24 in two different availability zones
* create 5 new ec2 instances based on Ubuntu 18.04 (bionic)
* deploy the following Java application on these instances
* create a load balancer for the Java application on port 80
* setup route53 to host CNAME record of elb url
---
# [Task 2](task02)
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
# [Task 3](task03)
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
# [Task 4](task04)
# Python CLI
* Please consider the work you submit here a small, but production-ready deliverable, in the sense that you are happy to ship such code, tests and documentation.
* Write a Roman numeral converter that converts integer numbers into Roman numerals:

```
func(36)

Output: "XXXVI"
```
---
# [Task 5](task05)
# Go tutorial on jupyter notebook
## Create html from ipynb
```bash
jupyter nbconvert --execute task05/go_tuturial.ipynb --to html
```
[html preview](https://htmlpreview.github.io/?https://github.com/titanlien/workshop/blob/master/task05/go_tuturial.html)

---
# [Task 6](task06)
## 6.1 Creare a ruby script
### It shows top 10 process in swap and sorts output by KB. It will ignore Zero values


## 6.2 Create a bach script

```
performs occasional test queries to the hostname "google.com" to each of the DNS servers configured in /etc/resolv.conf
```

## 6.3 Fix a client certificateds issue in nginx configure.


---
# [Task 7](task07)
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
# [Task 8](task08)
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

---
# [Task 12](task12)
### Provision kubeflow on minikube

---
# [Task 13](task13)
### Use FastAPI and sqlalchemy to create shortened URL similar to https://goo.gl/

---
# [Task 14](task14)
### Using terraform to create a private s3 bucket and a authorized user(IAM) to upload files. Using WhitelistIPs to grant user's exteral public IP address permission to access bucket.
#### :warning: When you provision this task, you can not depend on STS token. Because there is a lack support of STS to create a new IAM user. :warning:
```yml
# sample for whitelist to access s3 bucket
whitelistIPs = ["127.0.0.1/32"]
```

```bash
# get access_key from ssm
aws ssm get-parameter --name /system_user/backup-dev-uploader/access_key_id --with-decryption | jq .Parameter.Value

# get secret_key from ssm
aws ssm get-parameter --name /system_user/backup-dev-uploader/secret_access_key --with-decryption | jq .Parameter.Value

# terraform output
bucket_domain_name = "backup-dev-upload-task14.s3.amazonaws.com"
```
---
# [Task 15](task15)

You will find two applications: A Golang-based and a Java-based application. Both need to be
containerized according to industry best practices. The Golang application needs to be compiled from
source, while the Java application is delivered as a pre-built Jar file, runnable using Java 11.
Both are providing an HTTP service, binding to all interfaces on port 8080, with the same endpoints:
| Route | Description |
|-----------|---------------------------------------------------------------|
| / | A static site. Should *not* appear in the final setup |
| /hotels | JSON object containing hotel search results |
| /health | Exposes the health status of the application |
| /ready | Readiness probe |
| /metrics | Exposes Prometheus metrics of the application |

Your challenge will be to provide a load balancer setup like the following:
```bash
                            +------------------>Java app
                            |
                            |
                            |
                            30% of traffic
                            |
                            |
User +-------> load balancer+
                            |
                            |
                            70% of traffic
                            |
                            |
                            |
                            +------------------>Go app
```

The traffic distribution should be as follows: 70% of the requests are going to the application written in
Golang, 30% of the requests are going to the application written in Java. Also, each HTTP response needs
to carry a custom header, called x-trv-heritage which indicates the application that responded.
Your implementation must be runnable on a machine using x86_64 CPU architecture and must be built
on top of Kubernetes.
One should be able to at least see that the traffic distribution works as expected in some form. As a
bonus, you can try to show other metrics, like CPU usage, memory utilization, and latency as well to
compare the two services.
Your implementation should:

- Build both container images locally
- Find a solution to make them available to a Kubernetes cluster
- Do not push them to a public registry on the internet!
- Setup an ingress solution of your choice
- Deploy both workloads
- Wait for the readiness of the system
- Run 100 requests against / of the applications under test

---
# [Task 16](task16)
```bash
You are tasked with the creation of a small infrastructure stack on
AWS:
* Deploy a redundant and scalable EKS cluster
* Deploy on the cluster a simple Web Server application, exposing on
the public internet a simple home page with a custom message.
* Provide basic monitoring for your infrastructure *[Optional Task]*
* Increase the scalability of the stack *[Optional Task]*
* Provide cost estimations *[Optional Task]*
```

### Functional
#### EKS
* `EKS` cluster must consist of at least 3 `Worker Nodes`
* `Worker Nodes` should be distributed on at least `2 AZ`
* `Worker Nodes` should be assigned to at least `2 Worker Groups`
* You must run the latest version of `EKS-1.21`
#### Web Server
* Deploy, using `Helm`, a web server of your choice on the above
running cluster.
* The deployment should span the 2AZ where EKS nodes are spread, and
have a minimal redundancy.
* Customise the web server in order to show a home page with custom
message like "Hello bot, welcome to your simple web page"
* Expose securely the page in order to be reached from public internet

---
# [Task 17](task17)
* Present k8s with digitalocean provider, using resource digitalocean_kubernetes_cluster and digitalocean_kubernetes_node_pool.
* Deploy bitnami/nginx-ingress-controller helm chart by using resource helm_release.

---
# [Task 18](task18)
* A simple example to present how `helmfile` can depend on includeing vaules.yaml from different directory to share the common setting between landscape.
