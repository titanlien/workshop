FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

# for gunicorn in /start.sh
ENV PORT 5000
ENV BASE_URL http://localhost:5000/
ENV LOG_LEVEL WARNING
ENV WEB_CONCURRENCY 4

# Needed for proper functioning in Docker
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install pipenv

COPY Pipfile Pipfile.lock ./

RUN pipenv install --system --deploy

COPY app/*.py /app/app/
