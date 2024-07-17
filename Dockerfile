FROM python:3.8

ENV PYTHONUNBUFFERED 1

RUN mkdir -p /root/workspace
COPY requirements.txt /root/workspace/
WORKDIR /root/workspace/

RUN apt-get update \
    && apt-get install -y default-libmysqlclient-dev gcc

RUN pip install --upgrade pip \
    && pip install --upgrade setuptools \
    && pip install -r requirements.txt