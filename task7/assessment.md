**Dependency tools**

```
docker-engine
docker-compose
minikube
make
```

**Mandatory environemnt variables**

`SERVE_PORT`
default 5000

`GITHUB_TOKEN`
It's for pull docker private registry from github.com.

**Run app locally**

```
make install
pipenv shell
make run
```

**Run test within docker-compose**

```
make compose-test
```

**Run app on minikube**

```
make mini-run
```

**The api documents is on**

```
http://HOST:SERVE_PORT/docs
```

**The CI/CD pipeline is depend on github action.**

```
.github/
└── workflows
    ├── build_push.yml
    └── test.yml
```

**Demo**

[asciinema](https://asciinema.org/a/WYkoOC6m8SPKu8RKnkxqHE0Fc)
