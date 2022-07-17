FROM python:3.7

RUN apt-get -y update
RUN apt-get -y upgrade
RUN apt-get install -y sqlite3 libsqlite3-dev

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt --no-cache-dir

COPY . /app

WORKDIR /app

ENV FLASK_APP=src.app.py PYTHONUNBUFFERED=1
