"""Motor de precios del cotizador.

`calcular_cotizacion` es una función pura (solo lee de la base de datos, no
escribe nada) usada TANTO por el endpoint de preview (`/cotizador/calcular/`)
como por el de creación de solicitud (`/cotizador/solicitudes/`), para no
duplicar la lógica de cálculo entre las dos vistas.
"""
from decimal import Decimal

from contenido.models import Servicio

from .models import NivelRiesgoARL, PrecioServicio, RangoEmpleados


def _resolver_rango_empleados(numero_empleados):
    rangos = list(RangoEmpleados.objects.all().order_by("orden"))

    for rango in rangos:
        dentro_del_minimo = rango.empleados_min <= numero_empleados
        dentro_del_maximo = rango.empleados_max is None or numero_empleados <= rango.empleados_max
        if dentro_del_minimo and dentro_del_maximo:
            return rango

    # Fallback razonable si ningún rango calza exactamente: el de mayor
    # empleados_min que sea <= numero_empleados. No debe explotar aunque la
    # tabla de rangos esté vacía o mal configurada.
    candidatos = [r for r in rangos if r.empleados_min <= numero_empleados]
    if candidatos:
        return max(candidatos, key=lambda r: r.empleados_min)

    return None


def calcular_cotizacion(servicios_ids, numero_empleados, nivel_riesgo_id=None):
    rango = _resolver_rango_empleados(numero_empleados)

    multiplicador = Decimal("1.00")
    nivel_riesgo = None
    if nivel_riesgo_id:
        nivel_riesgo = NivelRiesgoARL.objects.filter(pk=nivel_riesgo_id).first()
        if nivel_riesgo is not None:
            multiplicador = nivel_riesgo.multiplicador

    servicios_por_id = {s.pk: s for s in Servicio.objects.filter(pk__in=servicios_ids)}

    items = []
    subtotal = Decimal("0.00")

    for servicio_id in servicios_ids:
        servicio = servicios_por_id.get(servicio_id)
        if servicio is None:
            # Id inexistente/inactivo: se ignora silenciosamente en vez de explotar.
            continue

        precio_final = None
        personalizado = True

        if rango is not None:
            precio_servicio = PrecioServicio.objects.filter(
                servicio=servicio, rango_empleados=rango,
            ).first()
            if precio_servicio is not None:
                precio_final = (precio_servicio.precio_base * multiplicador).quantize(Decimal("0.01"))
                personalizado = False

        items.append(
            {
                "servicio_id": servicio.pk,
                "servicio_nombre": servicio.nombre,
                "precio": precio_final,
                "personalizado": personalizado,
            }
        )

        if precio_final is not None:
            subtotal += precio_final

    total = subtotal

    return {
        "rango_empleados": (
            {"id": rango.pk, "nombre": rango.nombre} if rango is not None else None
        ),
        "nivel_riesgo": (
            {
                "id": nivel_riesgo.pk,
                "nombre": nivel_riesgo.nombre,
                "multiplicador": nivel_riesgo.multiplicador,
            }
            if nivel_riesgo is not None
            else None
        ),
        "items": items,
        "subtotal": subtotal,
        "total": total,
    }
