#!/usr/bin/env bash
set -e

echo "Aplicando migraciones..."
python manage.py migrate --noinput

if [ "$SEED_DEMO" = "true" ]; then
    echo "Cargando contenido de ejemplo (seed_demo_content)..."
    python manage.py seed_demo_content
fi

python manage.py ensure_admin

echo "Iniciando servidor..."
exec python manage.py runserver 0.0.0.0:8000
