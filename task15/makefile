PROJECT := task15
K3D_REGI_PRI := registry.localhost
K3D_REGI_PREFIX := k3d-
K3D_REGI := $(K3D_REGI_PREFIX)$(K3D_REGI_PRI)
K3D_REGI_PORT := 12345
TEST_LOOP := 100

.PHONY: build-go
build-go:
	docker build -t $(PROJECT)-go -f docker/go.Dockerfile .

.PHONY: build-java
build-java:
	docker build -t $(PROJECT)-java -f docker/java.Dockerfile .

.PHONY: build
build: build-go build-java

.PHONY: init_k3d_reg
init_k3d_reg:
	k3d registry list|grep $(K3D_REGI_PRI) || \
	k3d registry create $(K3D_REGI_PRI) --port $(K3D_REGI_PORT)

.PHONY: publish
publish: build init_k3d_reg
	docker tag $(PROJECT)-go:latest $(K3D_REGI):$(K3D_REGI_PORT)/$(PROJECT)-go:latest
	docker push $(K3D_REGI):$(K3D_REGI_PORT)/$(PROJECT)-go:latest
	docker tag $(PROJECT)-java:latest $(K3D_REGI):$(K3D_REGI_PORT)/$(PROJECT)-java:latest
	docker push $(K3D_REGI):$(K3D_REGI_PORT)/$(PROJECT)-java:latest

.PHONY: dist-clean
dist-clean:
	k3d registry delete $(K3D_REGI)
	k3d cluster delete --all
	yes y | docker system prune -f --volumes
	yes y | docker image prune -a

.PHONY: create_k3d
create_k3d: init_k3d_reg
	k3d cluster list | grep my-cluster || \
	k3d cluster create my-cluster --servers 1 --agents 3 --port 9080:80@loadbalancer \
	--port 9443:443@loadbalancer --api-port 6443 --k3s-arg "--disable=traefik@server:0" \
	--registry-use k3d-registry.localhost:12345

.PHONY: install_istio
install_istio:
	istioctl verify-install || yes y | istioctl install --set profile=default && \
		kubectl label namespace default istio-injection=enabled

.PHONY: deploy_app
deploy_app: install_istio
	kubectl apply -f k8s/

.PHONY: curl_get
curl_get:
	for i in `seq 1 $(TEST_LOOP)`; do \
    curl -sI http://localhost:9080/ready | grep x-trv-heritage ; \
  done

.PHONY: monitor
monitor:
	kubectl apply -f monitor/
