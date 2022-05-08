### Pre-installed packages list

|Application|Version|Download|
| :---:   | :-: | :-: |
|make|i386-apple-darwin11.3.0| OS default|
|docker desktop|4.7.1 (77678)|https://www.docker.com/products/docker-desktop/|
|k3d|v5.4.1|https://k3d.io/v5.4.1/#installation|
|kubectl|GitVersion:"v1.23.6"|https://kubernetes.io/docs/tasks/tools/#kubectl|
|istioctl|v1.13.3|https://istio.io/latest/docs/ops/diagnostic-tools/istioctl/#install-hahahugoshortcode-s2-hbhb|

---
## Manually step
* Because we can't resolve `*.locahost` to locahost(127.0.0.1) in MacOS. So we have to manually add k3d-registry.localhost's IP into `/etc/hosts` to allow to publish docker image into local k3d registry.
Only excute once.
```bash
sudo echo `127.0.0.1 k3d-registry.localhost` >> /etc/hosts
```
---
### Deployment workflow
```bash
# Compile go and java application into docker image
make build

# Create k3d docker registry
make init_k3d_reg

# Deploy local docker images to k3d registry
make publish

# Create k3d cluster and map host port 9080 to 80, port 9443 to 443 in cluster
make create_k3d

# Install istio ingress and enable auto side-car injection in default namespace
# Then apply deployment to k3d cluster
make deploy_app

# Deploy kiali, prometheus and grafa to visualize the traffic,
# refer to https://github.com/istio/istio/tree/master/samples/addons
make monitor

# Send GET request to /ready path and filter out its response header, x-trv-heritag
# You can setup TEST_LOOP to control how many times to test, default is 100.
make curl_get TEST_LOOP=<NUMBER>

# Port forwarding kiali to host
istioctl dashboard kiali

# Port forwarding grafara to host
kubectl port-forward svc/grafana -n istio-system 3000:3000
http://localhost:3000/ # open in browser
```

### Clean up all resources
```bash
make dist-clean
```
---
### Record
* [asciinema](https://asciinema.org/a/UFqYr829EegfEkxgkYUYLfYoK)
---
### Todo:
* Configure Golang(✅) and Java grafana dashboard to show metrics
* Migrate makefile to *.just file
* Migrate k8s directory to helm chart
* Install cert-manager to create SSL certificate (optional)
* Install external-DNS to register domain  (optional)
