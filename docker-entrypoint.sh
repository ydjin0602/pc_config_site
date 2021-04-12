#!/bin/sh

echo "Apply database migrations"
python manage.py migrate
uvicorn --host 0.0.0.0 --port 8000 pc_config_site.asgi:application