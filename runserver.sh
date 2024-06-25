#!/bin/sh
python manage.py migrate

gunicorn --bind 0.0.0.0:8000 --timeout 500 social_networking.asgi:application --max-requests 10 --max-requests-jitter 3 --keep-alive 10 -k uvicorn.workers.UvicornWorker --reload --log-level=info