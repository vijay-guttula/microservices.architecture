FROM python:3.9

ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN pip3 install -r requirements.txt

# RUN psql -c 'create database content_service;' -U ssvijayg

COPY . /app
