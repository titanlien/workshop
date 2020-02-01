# Init k8s with kind on your local desktop
* [Reference](https://kind.sigs.k8s.io/docs/user/quick-start/)
```
➤ kind create cluster --name dev
Creating cluster "dev" ...
 ✓ Ensuring node image (kindest/node:v1.17.0) 🖼
 ✓ Preparing nodes 📦
 ✓ Writing configuration 📜
 ✓ Starting control-plane 🕹️
 ✓ Installing CNI 🔌
 ✓ Installing StorageClass 💾
Set kubectl context to "kind-dev"
You can now use your cluster with:

kubectl cluster-info --context kind-dev

Have a nice day! 👋
17:40 ~/D/w/task3 [master]
➤ kubectl cluster-info --context kind-dev
Kubernetes master is running at https://127.0.0.1:32768
KubeDNS is running at https://127.0.0.1:32768/api/v1/namespaces/kube-system/services/kube-dns:dns/proxy

To further debug and diagnose cluster problems, use 'kubectl cluster-info dump'.
17:40 ~/D/w/task3 [master]
➤ kubectl config get-contexts
CURRENT   NAME                 CLUSTER          AUTHINFO         NAMESPACE
          docker-desktop       docker-desktop   docker-desktop
          docker-for-desktop   docker-desktop   docker-desktop
*         kind-dev             kind-dev         kind-dev
17:40 ~/D/w/task3 [master]
```
# install pipenv
* Please refer to [pipenv official website](https://pipenv.kennethreitz.org/en/latest/)
* then login pipenv, `pipenv shell && pipenv sync`

# Engine
* docker desktop version: 2.1.0.5
* kubectl client: v1.16.3
* kubectl server: v1.14.8
# Check kubectl context
```
kubectl config get-contexts
CURRENT   NAME                          CLUSTER          AUTHINFO           NAMESPACE
*         docker-desktop                docker-desktop   docker-desktop
          docker-for-desktop            docker-desktop   docker-desktop
          kops.mhlien.de                kops.mhlien.de   kops.mhlien.de
          kubernetes-admin@kubernetes   kubernetes       kubernetes-admin
```
# Run script
```
./deploy_webapp.sh
```

# Get webapp2 result
```
curl http://localhost:8080/
```

# Demo
https://asciinema.org/a/rlPRM7LwE76U84jCVx6rUO57l
