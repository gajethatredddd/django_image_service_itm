FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app/django_app

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       gcc python3-dev libpq-dev \
       tesseract-ocr tesseract-ocr-rus \
       libsm6 libxext6 libxrender-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .

RUN mkdir -p /app/django_app/static \
             /app/django_app/media \
             /app/django_app/logs \
             /app/django_app/geoip \
    && chmod -R 755 /app/django_app/static \
                   /app/django_app/media \
                   /app/django_app/logs \
                   /app/django_app/geoip

COPY geoip/GeoLite2-City.mmdb /app/django_app/geoip/
