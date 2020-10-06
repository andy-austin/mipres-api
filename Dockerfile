FROM python:3.6-slim

RUN apt-get update -y
RUN apt-get install -y git make gcc

WORKDIR /mipres-api
COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install --upgrade -r requirements.txt
RUN venv/bin/pip install gunicorn alembic eventlet
ENV PATH=/mipres-api/venv/bin:${PATH}
COPY . .
COPY ./k8s/entrypoint.sh .
RUN chmod +x entrypoint.sh

ENTRYPOINT sh entrypoint.sh
