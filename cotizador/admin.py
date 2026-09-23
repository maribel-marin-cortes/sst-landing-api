from django.contrib import admin

from .models import MensajeContacto, NivelRiesgoARL, PrecioServicio, RangoEmpleados, SolicitudCotizacion


@admin.register(RangoEmpleados)
class RangoEmpleadosAdmin(admin.ModelAdmin):
    list_display = ["nombre", "empleados_min", "empleados_max", "orden"]
    list_editable = ["orden"]


@admin.register(NivelRiesgoARL)
class NivelRiesgoARLAdmin(admin.ModelAdmin):
    list_display = ["nivel", "nombre", "multiplicador", "orden"]
    list_editable = ["multiplicador", "orden"]


@admin.register(PrecioServicio)
class PrecioServicioAdmin(admin.ModelAdmin):
    list_display = ["servicio", "rango_empleados", "precio_base"]
    list_editable = ["precio_base"]
    list_filter = ["servicio", "rango_empleados"]


@admin.register(SolicitudCotizacion)
class SolicitudCotizacionAdmin(admin.ModelAdmin):
    list_display = [
        "nombre_empresa",
        "nombre_contacto",
        "email_contacto",
        "numero_empleados",
        "estado",
        "precio_estimado_total",
        "creado_en",
    ]
    list_editable = ["estado"]
    list_filter = ["estado", "nivel_riesgo"]
    search_fields = ["nombre_empresa", "nit", "nombre_contacto", "email_contacto"]
    readonly_fields = ["precio_estimado_total", "creado_en"]
    filter_horizontal = ["servicios"]


@admin.register(MensajeContacto)
class MensajeContactoAdmin(admin.ModelAdmin):
    list_display = ["nombre", "email", "telefono", "creado_en"]
    readonly_fields = ["creado_en"]
    search_fields = ["nombre", "email"]
