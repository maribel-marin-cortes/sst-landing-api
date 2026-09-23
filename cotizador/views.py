import logging
from decimal import Decimal

from django.conf import settings
from django.core.mail import send_mail
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import MensajeContacto, NivelRiesgoARL, RangoEmpleados, SolicitudCotizacion
from .pricing import calcular_cotizacion
from .serializers import (
    CalcularCotizacionInputSerializer,
    CotizacionResultadoSerializer,
    MensajeContactoSerializer,
    NivelRiesgoARLSerializer,
    RangoEmpleadosSerializer,
    SolicitudCotizacionCreateSerializer,
)
from .throttles import ContactoThrottle, CotizadorCalcularThrottle, CotizadorSolicitudThrottle

logger = logging.getLogger(__name__)

_RESULTADO_VACIO = {
    "rango_empleados": None,
    "nivel_riesgo": None,
    "items": [],
    "subtotal": Decimal("0.00"),
    "total": Decimal("0.00"),
}


class RangoEmpleadosListView(generics.ListAPIView):
    queryset = RangoEmpleados.objects.all()
    serializer_class = RangoEmpleadosSerializer
    permission_classes = [AllowAny]


class NivelRiesgoARLListView(generics.ListAPIView):
    queryset = NivelRiesgoARL.objects.all()
    serializer_class = NivelRiesgoARLSerializer
    permission_classes = [AllowAny]


class CalcularCotizacionView(APIView):
    permission_classes = [AllowAny]
    throttle_classes = [CotizadorCalcularThrottle]
    throttle_scope = "cotizador_calcular"

    def post(self, request):
        serializer = CalcularCotizacionInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        if data.get("website"):
            # Honeypot: probablemente un bot. Responder 200 sin delatar la
            # detección, pero sin ejecutar el cálculo real.
            return Response(CotizacionResultadoSerializer(_RESULTADO_VACIO).data)

        resultado = calcular_cotizacion(
            servicios_ids=data["servicios"],
            numero_empleados=data["numero_empleados"],
            nivel_riesgo_id=data.get("nivel_riesgo_id"),
        )
        return Response(CotizacionResultadoSerializer(resultado).data)


class SolicitudCotizacionCreateView(generics.CreateAPIView):
    queryset = SolicitudCotizacion.objects.all()
    serializer_class = SolicitudCotizacionCreateSerializer
    permission_classes = [AllowAny]
    throttle_classes = [CotizadorSolicitudThrottle]
    throttle_scope = "cotizador_solicitud"

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if serializer.validated_data.pop("website", ""):
            # Honeypot: no guardar nada ni enviar email, pero responder 200
            # igual para no delatarle al bot que fue detectado.
            return Response({}, status=status.HTTP_200_OK)

        servicios = serializer.validated_data.pop("servicios", [])
        nivel_riesgo = serializer.validated_data.get("nivel_riesgo")

        # El precio SIEMPRE se recalcula en el servidor con el mismo motor que
        # usa el preview — nunca se confía en un precio que mande el cliente
        # (de hecho el serializer de entrada ni siquiera acepta ese campo).
        resultado = calcular_cotizacion(
            servicios_ids=[servicio.pk for servicio in servicios],
            numero_empleados=serializer.validated_data.get("numero_empleados"),
            nivel_riesgo_id=nivel_riesgo.pk if nivel_riesgo else None,
        )

        solicitud = serializer.save(precio_estimado_total=resultado["total"])
        solicitud.servicios.set(servicios)

        self._enviar_notificacion(solicitud)

        output = SolicitudCotizacionCreateSerializer(solicitud, context={"request": request})
        headers = self.get_success_headers(output.data)
        return Response(output.data, status=status.HTTP_201_CREATED, headers=headers)

    def _enviar_notificacion(self, solicitud):
        try:
            send_mail(
                subject=f"Nueva solicitud de cotización — {solicitud.nombre_empresa}",
                message=(
                    f"Empresa: {solicitud.nombre_empresa}\n"
                    f"NIT: {solicitud.nit}\n"
                    f"Sector: {solicitud.sector}\n"
                    f"Número de empleados: {solicitud.numero_empleados}\n"
                    f"Contacto: {solicitud.nombre_contacto} ({solicitud.cargo_contacto})\n"
                    f"Email: {solicitud.email_contacto}\n"
                    f"Teléfono: {solicitud.telefono_contacto}\n"
                    f"Precio estimado total: {solicitud.precio_estimado_total}\n"
                    f"Comentario: {solicitud.comentario}\n"
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.NOTIFICACIONES_EMAIL],
                fail_silently=False,
            )
        except Exception:
            # El registro en BD ya se guardó y es la fuente de verdad: un
            # fallo de SMTP nunca debe traducirse en un 500 para el usuario.
            logger.exception(
                "Fallo enviando email de notificación de nueva solicitud de cotización (id=%s)",
                solicitud.pk,
            )


class MensajeContactoCreateView(generics.CreateAPIView):
    queryset = MensajeContacto.objects.all()
    serializer_class = MensajeContactoSerializer
    permission_classes = [AllowAny]
    throttle_classes = [ContactoThrottle]
    throttle_scope = "contacto"

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if serializer.validated_data.pop("website", ""):
            return Response({}, status=status.HTTP_200_OK)

        mensaje = serializer.save()
        self._enviar_notificacion(mensaje)

        output = MensajeContactoSerializer(mensaje)
        headers = self.get_success_headers(output.data)
        return Response(output.data, status=status.HTTP_201_CREATED, headers=headers)

    def _enviar_notificacion(self, mensaje):
        try:
            send_mail(
                subject=f"Nuevo mensaje de contacto — {mensaje.nombre}",
                message=(
                    f"Nombre: {mensaje.nombre}\n"
                    f"Email: {mensaje.email}\n"
                    f"Teléfono: {mensaje.telefono}\n\n"
                    f"{mensaje.mensaje}"
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.NOTIFICACIONES_EMAIL],
                fail_silently=False,
            )
        except Exception:
            logger.exception(
                "Fallo enviando email de notificación de nuevo mensaje de contacto (id=%s)",
                mensaje.pk,
            )
