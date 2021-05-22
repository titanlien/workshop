FROM python:3.9.4-slim as base

RUN pip install pipenv

WORKDIR /authorizer

COPY Pipfile Pipfile.lock ./

RUN pipenv install --system

FROM base as test

RUN pipenv install --dev --system

COPY authorizer ./authorizer

COPY tests ./tests

RUN python -m pytest -m "not integration" -vv --junitxml=result.xml --cov-report term-missing --cov-report xml:coverage.xml --cov=authorizer tests/

FROM base as release

COPY authorizer ./authorizer

COPY entrypoint.sh operations ./

ENTRYPOINT [ "/authorizer/entrypoint.sh" ]
