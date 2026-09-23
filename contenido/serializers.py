from rest_framework import serializers

from .models import ConfiguracionSitio, HitoHistoria, LogoCliente, MiembroEquipo, Servicio


class ConfiguracionSitioSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConfiguracionSitio
        fields = "__all__"


class HitoHistoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = HitoHistoria
        fields = "__all__"


class MiembroEquipoSerializer(serializers.ModelSerializer):
    class Meta:
        model = MiembroEquipo
        fields = "__all__"


class ServicioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Servicio
        fields = "__all__"


class LogoClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = LogoCliente
        fields = "__all__"
