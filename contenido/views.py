from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import ConfiguracionSitio, HitoHistoria, LogoCliente, MiembroEquipo, Servicio
from .serializers import (
    ConfiguracionSitioSerializer,
    HitoHistoriaSerializer,
    LogoClienteSerializer,
    MiembroEquipoSerializer,
    ServicioSerializer,
)


class ConfiguracionSitioView(APIView):
    """Expone el único registro de ConfiguracionSitio (pensado como singleton).
    404 si todavía no se ha corrido el seed / no se ha creado desde /admin."""

    permission_classes = [AllowAny]

    def get(self, request):
        configuracion = ConfiguracionSitio.objects.first()
        if configuracion is None:
            return Response(
                {"detail": "No hay configuración del sitio registrada todavía."},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = ConfiguracionSitioSerializer(configuracion, context={"request": request})
        return Response(serializer.data)


class HitoHistoriaViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = HitoHistoria.objects.all()
    serializer_class = HitoHistoriaSerializer
    permission_classes = [AllowAny]


class MiembroEquipoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = MiembroEquipo.objects.filter(activo=True)
    serializer_class = MiembroEquipoSerializer
    permission_classes = [AllowAny]


class ServicioViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Servicio.objects.filter(activo=True)
    serializer_class = ServicioSerializer
    permission_classes = [AllowAny]


class LogoClienteViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = LogoCliente.objects.filter(activo=True)
    serializer_class = LogoClienteSerializer
    permission_classes = [AllowAny]
