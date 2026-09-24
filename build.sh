#!/usr/bin/env bash
# Build command que corre Render antes de cada deploy.
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate

# Igual que en docker local (entrypoint.sh): opt-in via env var, e
# idempotente (get_or_create), no pisa contenido que ya hayas editado en
# /admin.
if [ "$SEED_DEMO" = "true" ]; then
    python manage.py seed_demo_content
fi

python manage.py ensure_admin
