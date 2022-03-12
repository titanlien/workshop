FROM tiangolo/uvicorn-gunicorn:python3.7

# for gunicorn in /start.sh
ENV PORT 5000
# for application level
ENV SERVE_PORT 5000

ENV WEB_CONCURRENCY 4

# Needed for proper functioning in Docker
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install pipenv

COPY Pipfile Pipfile.lock ./

RUN pipenv install --system --deploy

COPY app/* /app/app/
