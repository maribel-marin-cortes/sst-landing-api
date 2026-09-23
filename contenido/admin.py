from django.contrib import admin

from .models import ConfiguracionSitio, HitoHistoria, LogoCliente, MiembroEquipo, Servicio


@admin.register(ConfiguracionSitio)
class ConfiguracionSitioAdmin(admin.ModelAdmin):
    list_display = ["nombre_empresa", "correo_contacto", "whatsapp_numero", "telefono"]

    def has_add_permission(self, request):
        # Singleton: no permitir crear un segundo registro si ya existe uno.
        if ConfiguracionSitio.objects.exists():
            return False
        return super().has_add_permission(request)


@admin.register(HitoHistoria)
class HitoHistoriaAdmin(admin.ModelAdmin):
    list_display = ["anio", "titulo", "orden"]
    list_editable = ["orden"]
    ordering = ["orden", "anio"]


@admin.register(MiembroEquipo)
class MiembroEquipoAdmin(admin.ModelAdmin):
    list_display = ["nombre", "cargo", "profesion", "activo", "orden"]
    list_editable = ["activo", "orden"]
    list_filter = ["activo"]
    search_fields = ["nombre", "cargo", "profesion"]


@admin.register(Servicio)
class ServicioAdmin(admin.ModelAdmin):
    list_display = ["nombre", "slug", "normativa", "destacado", "activo", "orden"]
    list_editable = ["destacado", "activo", "orden"]
    list_filter = ["activo", "destacado"]
    search_fields = ["nombre", "normativa"]
    prepopulated_fields = {"slug": ("nombre",)}


@admin.register(LogoCliente)
class LogoClienteAdmin(admin.ModelAdmin):
    list_display = ["nombre", "url_sitio", "activo", "orden"]
    list_editable = ["activo", "orden"]
    list_filter = ["activo"]
