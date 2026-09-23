from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r"historia", views.HitoHistoriaViewSet, basename="historia")
router.register(r"equipo", views.MiembroEquipoViewSet, basename="equipo")
router.register(r"servicios", views.ServicioViewSet, basename="servicios")
router.register(r"clientes", views.LogoClienteViewSet, basename="clientes")

urlpatterns = [
    path("config/", views.ConfiguracionSitioView.as_view(), name="configuracion-sitio"),
] + router.urls
