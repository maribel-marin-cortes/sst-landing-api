from rest_framework import serializers

from contenido.models import Servicio

from .models import MensajeContacto, NivelRiesgoARL, RangoEmpleados, SolicitudCotizacion


class RangoEmpleadosSerializer(serializers.ModelSerializer):
    class Meta:
        model = RangoEmpleados
        fields = "__all__"


class NivelRiesgoARLSerializer(serializers.ModelSerializer):
    class Meta:
        model = NivelRiesgoARL
        fields = "__all__"


# --- Resultado de calcular_cotizacion() (usado por /calcular/ y como parte de
# la respuesta de referencia; no está atado a un modelo, es un dict). ---


class CotizacionItemSerializer(serializers.Serializer):
    servicio_id = serializers.IntegerField()
    servicio_nombre = serializers.CharField()
    precio = serializers.DecimalField(max_digits=12, decimal_places=2, allow_null=True)
    personalizado = serializers.BooleanField()


class RangoEmpleadosResumenSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    nombre = serializers.CharField()


class NivelRiesgoResumenSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    nombre = serializers.CharField()
    multiplicador = serializers.DecimalField(max_digits=4, decimal_places=2)


class CotizacionResultadoSerializer(serializers.Serializer):
    rango_empleados = RangoEmpleadosResumenSerializer(allow_null=True)
    nivel_riesgo = NivelRiesgoResumenSerializer(allow_null=True)
    items = CotizacionItemSerializer(many=True)
    subtotal = serializers.DecimalField(max_digits=14, decimal_places=2)
    total = serializers.DecimalField(max_digits=14, decimal_places=2)


class CalcularCotizacionInputSerializer(serializers.Serializer):
    numero_empleados = serializers.IntegerField(min_value=1)
    nivel_riesgo_id = serializers.IntegerField(required=False, allow_null=True)
    servicios = serializers.ListField(child=serializers.IntegerField(), allow_empty=False)
    # Honeypot anti-bot: si llega con contenido, la vista responde 200 sin
    # ejecutar el cálculo real (ver CalcularCotizacionView.post).
    website = serializers.CharField(required=False, allow_blank=True, write_only=True)


class SolicitudCotizacionCreateSerializer(serializers.ModelSerializer):
    servicios = serializers.PrimaryKeyRelatedField(queryset=Servicio.objects.all(), many=True)
    # Honeypot anti-bot: si llega con contenido, la vista no guarda nada ni
    # envía email, pero responde 200 igual (ver SolicitudCotizacionCreateView.create).
    website = serializers.CharField(required=False, allow_blank=True, write_only=True)

    class Meta:
        model = SolicitudCotizacion
        fields = [
            "id",
            "nombre_empresa",
            "nit",
            "sector",
            "numero_empleados",
            "nivel_riesgo",
            "servicios",
            "nombre_contacto",
            "cargo_contacto",
            "email_contacto",
            "telefono_contacto",
            "comentario",
            "precio_estimado_total",
            "estado",
            "creado_en",
            "website",
        ]
        read_only_fields = ["id", "precio_estimado_total", "estado", "creado_en"]


class MensajeContactoSerializer(serializers.ModelSerializer):
    # Honeypot anti-bot (ver MensajeContactoCreateView.create).
    website = serializers.CharField(required=False, allow_blank=True, write_only=True)

    class Meta:
        model = MensajeContacto
        fields = ["id", "nombre", "email", "telefono", "mensaje", "creado_en", "website"]
        read_only_fields = ["id", "creado_en"]
