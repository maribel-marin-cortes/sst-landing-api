#!/usr/bin/env bash
# Build command que corre Render antes de cada deploy.
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate
