#!/bin/bash

pip install --no-cache-dir -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
gunicorn student_performance1.wsgi --bind 0.0.0.0:8000
