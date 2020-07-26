FROM tiangolo/uvicorn-gunicorn:python3.7

RUN pip install pipenv

WORKDIR /app

EXPOSE 5000

ENV PORT 5000

ENV HOST 0.0.0.0

COPY Pipfile Pipfile.lock main.py ./

RUN pipenv install --system --deploy
