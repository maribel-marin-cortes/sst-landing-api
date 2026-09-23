from rest_framework.throttling import AnonRateThrottle


class CotizadorCalcularThrottle(AnonRateThrottle):
    scope = "cotizador_calcular"


class CotizadorSolicitudThrottle(AnonRateThrottle):
    scope = "cotizador_solicitud"


class ContactoThrottle(AnonRateThrottle):
    scope = "contacto"
