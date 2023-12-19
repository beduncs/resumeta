FROM python:3.11

ENV DATABASE_URL mongodb://mongo:27017

WORKDIR /code

COPY . /code

RUN pip3 --no-cache-dir install poetry && poetry install

CMD ["poetry", "run", "uvicorn", "server.main:app", "--host", "0.0.0.0", "--port", "8080"]
