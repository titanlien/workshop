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
	rm -f ${TEST_RESULT_XML_PATH} ${COVERAGE_XML_PATH} .coverage test.db sql_app.db

.PHONY: install
install:
	pipenv install

.PHONY: run
run:
	uvicorn app.main:app --reload --port 5000 --host 0.0.0.0 --debug

.PHONY: test-deps
test-deps:
	pipenv install --dev

.PHONY: test
test: clean
	python3 -m pytest $(PYTEST_SETTINGS) tests/

.PHONY: compose-down
compose-down:
	docker-compose down || true

.PHONY: compose-up
compose-up: compose-down
	docker-compose up --build -d
