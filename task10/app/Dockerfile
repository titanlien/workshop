FROM tiangolo/uvicorn-gunicorn:python3.7 as base

RUN pip install pipenv

WORKDIR /app

COPY Pipfile Pipfile.lock ./

RUN pipenv install --system --deploy

From base as test

RUN pipenv install --dev --system

COPY main.py test_main.py ./

RUN python -m pytest test_main.py

FROM base as release

COPY main.py ./

EXPOSE 5000

ENV PORT 5000

ENV HOST 0.0.0.0
