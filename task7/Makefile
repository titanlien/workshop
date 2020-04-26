TEST_RESULT_XML_PATH ?= result.xml
COVERAGE_XML_PATH ?= coverage.xml
PROJECT = app

PYTEST_SETTINGS = -vv --junitxml=$(TEST_RESULT_XML_PATH) \
	--cov-report term-missing --cov-report xml:$(COVERAGE_XML_PATH) --cov=$(PROJECT)


.PHONY: clean-pyc
clean-pyc:
	find . -name '*.pyc' -delete

.PHONY: clean
clean: clean-pyc
	rm -f ${TEST_RESULT_XML_PATH} ${COVERAGE_XML_PATH}

.PHONY: install
install:
	pipenv install

.PHONY: test-dependencies
test-dependencies:
	pipenv install --dev

.PHONY: local-test
local-test: clean
	docker-compose down -v
	docker-compose up -d mongo
	python3 -m pytest $(PYTEST_SETTINGS) tests/
	docker-compose down -v

.PHONY: pre-commit-install
pre-commit-install:
	pip3 install pre-commit
	pre-commit install

.PHONY: check
check: pre-commit-install
	pre-commit run --all-files

.PHONY: run
run:
	docker-compose up -d mongo
	uvicorn app.main:app --reload --port ${SERVE_PORT}

.PHONY: compose-test
compose-test:
	docker-compose down -v
	docker-compose -f docker-compose.yml -f docker-compose.test.yml up --build --abort-on-container-exit

.PHONY: test
test: clean
	python3 -m pytest $(PYTEST_SETTINGS) tests/

.PHONY: compose-down
compose-down:
	docker-compose down || true

.PHONY: compose-up
compose-up: compose-down
	docker-compose up --build -d

.PHONY: mini-run
mini-run:
	kubectl create secret docker-registry regcred --docker-server=docker.pkg.github.com --docker-username=titanlien --docker-password=${GITHUB_TOKEN} || true
	helm install local -f helm/mongo_values.yaml bitnami/mongodb
	kubectl apply -f ./kube
	minikube service --url webapp-svc
