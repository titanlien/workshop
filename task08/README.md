# Canary deploy with istio and minikube
---

### This task is excuting `kubectl apply` the manifest files by serial number order.
```bash
kubectl apply -f 1-istio-init.yaml
kubectl apply -f 2-istio-minikube.yaml
...
```

### export nodePort of ingress gateway and minikube ip
```bash
export INGRESS_PORT=$(kubectl -n istio-system get service istio-ingressgateway -o jsonpath='{.spec.ports[?(@.name=="http2")].nodePort}')
export INGRESS_HOST=$(minikube ip)
```

### gather the app's version by curl
```bash
while curl http://$INGRESS_HOST:$INGRESS_PORT/ -HHost:demo.local; sleep 0.5; end
```
#Demo on kiali
### prod:dev = 9:1
![prod:dev=9:1](images/9-1.png)
### prod:dev = 1:1
![prod:dev=1:1](images/1-1.png)


[Record](https://asciinema.org/a/qVQVhiBr66To4uyShZe20IuCq)
