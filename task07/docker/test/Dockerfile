FROM python:3.10.4

# To enable the --no-cache-dir, a falsy value is needed
ENV PIP_NO_CACHE_DIR false

RUN pip3 install pipenv

WORKDIR /usr/src/app

COPY Pipfile Pipfile.lock ./

RUN pipenv install --dev --system --deploy

COPY . .
