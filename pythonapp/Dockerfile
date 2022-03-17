# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

WORKDIR /pythonapp

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

VOLUME /pythonapp

CMD [ "python", "pythonapp.py" ]
