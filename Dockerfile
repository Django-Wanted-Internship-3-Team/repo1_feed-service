FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV POETRY_HOME=/etc/poetry python3 -


RUN mkdir /app/
WORKDIR /app/

RUN apt update
RUN pip install "poetry==1.6.1"
RUN poetry install

COPY pyproject.toml .

RUN poetry install

COPY . /app
