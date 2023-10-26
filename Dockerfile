FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir /app/
WORKDIR /app/

RUN apt update
COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY pyproject.toml .

RUN poetry install

COPY . /app
