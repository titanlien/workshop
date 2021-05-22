TEST_RESULT_XML_PATH ?= result.xml
COVERAGE_XML_PATH ?= coverage.xml
PROJECT = authorizer

PYTEST_SETTINGS = -vv --junitxml=$(TEST_RESULT_XML_PATH) \
  --cov-report term-missing --cov-report xml:$(COVERAGE_XML_PATH) --cov=$(PROJECT)

.PHONY: install
install:
	pip3 install pipenv
	pipenv install --dev
	pipenv shell

.PHONY: clean-pyc
clean-pyc:
	find . -name '*.pyc' -delete

.PHONY: clean
clean: clean-pyc
	rm -rf $(PROJECT).egg-info $(COVERAGE_XML_PATH) $(TEST_RESULT_XML_PATH)

.PHONY: dist-clean
dist-clean: clean
	pipenv --rm

.PHONY: test
test: clean
	python -m pytest -m "not integration" $(PYTEST_SETTINGS) tests/

.PHONE: build
build:
	docker build -t $(PROJECT) .

.PHONE: run
run: build
	docker run --rm -e LOG_LEVEL=WARN $(PROJECT)
