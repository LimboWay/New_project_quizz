FROM python:3.10.10-slim

RUN apt update
RUN apt install -y python3-dev
RUN apt install -y libpq-dev
RUN apt install -y gcc
RUN apt install -y curl
RUN apt install -y mc
RUN apt install -y vim

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRIREBYTECODE 1

RUN mkdir /opt/src
WORKDIR /opt/src

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN rm -f requirements.txt

COPY src .

EXPOSE 8890
