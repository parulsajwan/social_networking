FROM python:latest AS builder

WORKDIR /app
COPY requirements /app/requirements
ARG requirement=/app/requirements/development.txt
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    bash git gcc musl-dev python3-dev swig libpq-dev build-essential supervisor vim telnet postgresql-client libqpdf-dev gdal-bin && \
    rm -rf /var/lib/apt/lists/*

RUN python -m pip install --upgrade pip setuptools wheel && \
    python -m pip install --no-cache-dir --default-timeout=100 -r ${requirement}


FROM builder AS deployer
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . .
