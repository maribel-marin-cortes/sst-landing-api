from decouple import config
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = (
        "Crea un superusuario a partir de DJANGO_SUPERUSER_USERNAME/EMAIL/PASSWORD "
        "si no existe todavía. Idempotente y silencioso si las variables no están "
        "definidas -- pensado para correr en cada build de Render (plan free, sin "
        "Shell) igual que build.sh."
    )

    def handle(self, *args, **options):
        username = config("DJANGO_SUPERUSER_USERNAME", default="")
        email = config("DJANGO_SUPERUSER_EMAIL", default="")
        password = config("DJANGO_SUPERUSER_PASSWORD", default="")

        if not username or not password:
            self.stdout.write("DJANGO_SUPERUSER_USERNAME/PASSWORD no definidas, se omite ensure_admin.")
            return

        User = get_user_model()
        if User.objects.filter(username=username).exists():
            self.stdout.write(f"Superusuario '{username}' ya existe, se omite.")
            return

        User.objects.create_superuser(username=username, email=email, password=password)
        self.stdout.write(self.style.SUCCESS(f"Superusuario '{username}' creado."))
