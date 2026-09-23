from decimal import Decimal

from django.db import models

from contenido.models import Servicio


class RangoEmpleados(models.Model):
    nombre = models.CharField(max_length=100)
    empleados_min = models.PositiveIntegerField()
    empleados_max = models.PositiveIntegerField(
        null=True, blank=True, help_text="Vacío/null significa 'sin tope' (o más).",
    )
    orden = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["orden"]
        verbose_name = "Rango de empleados"
        verbose_name_plural = "Rangos de empleados"

    def __str__(self):
        return self.nombre


class NivelRiesgoARL(models.Model):
    NIVEL_I = "I"
    NIVEL_II = "II"
    NIVEL_III = "III"
    NIVEL_IV = "IV"
    NIVEL_V = "V"
    NIVEL_CHOICES = [
        (NIVEL_I, "I"),
        (NIVEL_II, "II"),
        (NIVEL_III, "III"),
        (NIVEL_IV, "IV"),
        (NIVEL_V, "V"),
    ]

    nivel = models.CharField(max_length=3, choices=NIVEL_CHOICES)
    nombre = models.CharField(max_length=150)
    multiplicador = models.DecimalField(max_digits=4, decimal_places=2, default=Decimal("1.00"))
    orden = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["orden"]
        verbose_name = "Nivel de riesgo ARL"
        verbose_name_plural = "Niveles de riesgo ARL"

    def __str__(self):
        return self.nombre


class PrecioServicio(models.Model):
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE, related_name="precios")
    rango_empleados = models.ForeignKey(RangoEmpleados, on_delete=models.CASCADE, related_name="precios")
    precio_base = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        unique_together = ("servicio", "rango_empleados")
        verbose_name = "Precio de servicio"
        verbose_name_plural = "Precios de servicios"

    def __str__(self):
        return f"{self.servicio} — {self.rango_empleados}: {self.precio_base}"


class SolicitudCotizacion(models.Model):
    ESTADO_NUEVA = "NUEVA"
    ESTADO_CONTACTADO = "CONTACTADO"
    ESTADO_CONVERTIDA = "CONVERTIDA"
    ESTADO_DESCARTADA = "DESCARTADA"
    ESTADO_CHOICES = [
        (ESTADO_NUEVA, "Nueva"),
        (ESTADO_CONTACTADO, "Contactado"),
        (ESTADO_CONVERTIDA, "Convertida"),
        (ESTADO_DESCARTADA, "Descartada"),
    ]

    nombre_empresa = models.CharField(max_length=200)
    nit = models.CharField(max_length=30, blank=True)
    sector = models.CharField(max_length=150, blank=True, help_text='Texto libre, ej: "Comercio", "Construcción".')
    numero_empleados = models.PositiveIntegerField()
    nivel_riesgo = models.ForeignKey(
        NivelRiesgoARL, on_delete=models.SET_NULL, null=True, blank=True,
    )
    servicios = models.ManyToManyField(Servicio, related_name="solicitudes")
    nombre_contacto = models.CharField(max_length=200)
    cargo_contacto = models.CharField(max_length=150, blank=True)
    email_contacto = models.EmailField()
    telefono_contacto = models.CharField(max_length=30, blank=True)
    comentario = models.TextField(blank=True)
    precio_estimado_total = models.DecimalField(
        max_digits=14, decimal_places=2, null=True, blank=True,
        help_text="Calculado en el servidor, nunca se confía en un valor enviado por el cliente.",
    )
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default=ESTADO_NUEVA)
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-creado_en"]
        verbose_name = "Solicitud de cotización"
        verbose_name_plural = "Solicitudes de cotización"

    def __str__(self):
        return f"{self.nombre_empresa} ({self.creado_en:%Y-%m-%d})"


class MensajeContacto(models.Model):
    nombre = models.CharField(max_length=200)
    email = models.EmailField()
    telefono = models.CharField(max_length=30, blank=True)
    mensaje = models.TextField()
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-creado_en"]
        verbose_name = "Mensaje de contacto"
        verbose_name_plural = "Mensajes de contacto"

    def __str__(self):
        return f"{self.nombre} <{self.email}>"
