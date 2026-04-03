#!/bin/sh
set -e

echo "==> Applying database migrations..."
python manage.py migrate --noinput

echo "==> Loading fixtures..."
python manage.py loaddata data.json

echo "==> Starting server..."
exec gunicorn cookbook_project.wsgi:application --bind 0.0.0.0:$PORT --workers 2
