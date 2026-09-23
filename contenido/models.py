from django.db import models


class ConfiguracionSitio(models.Model):
    """Pensado como singleton: un único registro. Ver ConfiguracionSitioAdmin
    (bloquea crear un segundo) y ConfiguracionSitioView (expone el primero/único)."""

    nombre_empresa = models.CharField(max_length=200)
    eslogan = models.CharField(max_length=300)
    mision = models.TextField()
    vision = models.TextField()
    historia_titulo = models.CharField(max_length=200)
    historia_texto = models.TextField()
    hero_titulo = models.CharField(max_length=200)
    hero_subtitulo = models.CharField(max_length=300)
    hero_imagen = models.ImageField(upload_to="hero/", blank=True, null=True)
    logo = models.ImageField(upload_to="logo/", blank=True, null=True)
    whatsapp_numero = models.CharField(
        max_length=20,
        help_text="Solo dígitos con código de país, ej: 573001234567",
    )
    correo_contacto = models.EmailField()
    telefono = models.CharField(max_length=30, blank=True)
    direccion = models.CharField(max_length=255, blank=True)
    facebook_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)

    class Meta:
        verbose_name = "Configuración del sitio"
        verbose_name_plural = "Configuración del sitio"

    def __str__(self):
        return self.nombre_empresa or "Configuración del sitio"


class HitoHistoria(models.Model):
    anio = models.PositiveIntegerField()
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    orden = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["orden", "anio"]
        verbose_name = "Hito de historia"
        verbose_name_plural = "Hitos de historia"

    def __str__(self):
        return f"{self.anio} — {self.titulo}"


class MiembroEquipo(models.Model):
    nombre = models.CharField(max_length=200)
    cargo = models.CharField(max_length=200)
    profesion = models.CharField(max_length=200)
    tarjeta_profesional = models.CharField(
        max_length=100, blank=True,
        help_text="Número de tarjeta profesional / matrícula",
    )
    foto = models.ImageField(upload_to="equipo/", blank=True, null=True)
    bio = models.TextField()
    linkedin_url = models.URLField(blank=True)
    orden = models.PositiveIntegerField(default=0)
    activo = models.BooleanField(default=True)

    class Meta:
        ordering = ["orden"]
        verbose_name = "Miembro del equipo"
        verbose_name_plural = "Miembros del equipo"

    def __str__(self):
        return f"{self.nombre} ({self.cargo})"


class Servicio(models.Model):
    nombre = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    icono = models.CharField(
        max_length=100, blank=True, help_text="Nombre de un icono, ej: shield-check",
    )
    descripcion_corta = models.CharField(max_length=300)
    descripcion_larga = models.TextField()
    normativa = models.CharField(
        max_length=200, blank=True, help_text="Ej: Resolución 0312 de 2019",
    )
    destacado = models.BooleanField(default=False)
    orden = models.PositiveIntegerField(default=0)
    activo = models.BooleanField(default=True)

    class Meta:
        ordering = ["orden"]
        verbose_name = "Servicio"
        verbose_name_plural = "Servicios"

    def __str__(self):
        return self.nombre


class LogoCliente(models.Model):
    nombre = models.CharField(max_length=200)
    logo = models.ImageField(upload_to="clientes/")
    url_sitio = models.URLField(blank=True)
    orden = models.PositiveIntegerField(default=0)
    activo = models.BooleanField(default=True)

    class Meta:
        ordering = ["orden"]
        verbose_name = "Logo de cliente"
        verbose_name_plural = "Logos de clientes"

    def __str__(self):
        return self.nombre
