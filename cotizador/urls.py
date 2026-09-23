from django.urls import path

from . import views

urlpatterns = [
    path("rangos-empleados/", views.RangoEmpleadosListView.as_view(), name="rangos-empleados"),
    path("niveles-riesgo/", views.NivelRiesgoARLListView.as_view(), name="niveles-riesgo"),
    path("calcular/", views.CalcularCotizacionView.as_view(), name="cotizador-calcular"),
    path("solicitudes/", views.SolicitudCotizacionCreateView.as_view(), name="cotizador-solicitudes"),
]

# Montado aparte en config/urls.py bajo el prefijo /api/contacto/ (MensajeContacto
# vive en este app porque es lo que el sitio RECIBE, pero su URL pública no
# cuelga de /api/cotizador/).
contacto_urlpatterns = [
    path("mensajes/", views.MensajeContactoCreateView.as_view(), name="contacto-mensajes"),
]
