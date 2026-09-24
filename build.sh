#!/usr/bin/env bash
# Build command que corre Render antes de cada deploy.
set -o errexit

pip install -r requirements.txt

# --upload-unhashed-files: django-cloudinary-storage trae su propio
# collectstatic que, si no se usa SU storage para estaticos (solo lo usamos
# para MEDIA), hace de copy_file un no-op silencioso -- "0 static files
# copied" sin ningun error, el admin queda sin CSS/JS. Esta bandera lo
# desactiva y restaura el copiado normal de Django.
python manage.py collectstatic --noinput --upload-unhashed-files
python manage.py migrate

# Igual que en docker local (entrypoint.sh): opt-in via env var, e
# idempotente (get_or_create), no pisa contenido que ya hayas editado en
# /admin.
if [ "$SEED_DEMO" = "true" ]; then
    python manage.py seed_demo_content
fi

python manage.py ensure_admin
