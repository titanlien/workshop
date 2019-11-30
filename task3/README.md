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