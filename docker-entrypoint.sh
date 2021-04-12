#!/bin/sh

echo "Apply database migrations"
python manage.py migrate
gunicorn -b 0.0.0.0:8000 pc_config_site.wsgi --workers=5 --threads=2