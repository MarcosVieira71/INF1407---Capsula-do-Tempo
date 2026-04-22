#!/bin/sh

set -e

cd /app/capsula_tempo

python manage.py migrate --noinput
python manage.py collectstatic --noinput

gunicorn capsula_tempo.wsgi:application \
  --bind 0.0.0.0:8000 \
  --access-logfile - \
  --error-logfile - \
  --capture-output \
  --enable-stdio-inheritance