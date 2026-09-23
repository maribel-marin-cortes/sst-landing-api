from decimal import Decimal

from django.core.management.base import BaseCommand

from contenido.models import ConfiguracionSitio, HitoHistoria, LogoCliente, MiembroEquipo, Servicio
from cotizador.models import NivelRiesgoARL, PrecioServicio, RangoEmpleados


class Command(BaseCommand):
    help = "Carga contenido de ejemplo (placeholder) para la landing de SST. Idempotente."

    def handle(self, *args, **options):
        self._seed_configuracion()
        self._seed_historia()
        self._seed_equipo()
        servicios = self._seed_servicios()
        self._seed_clientes()
        rangos = self._seed_rangos_empleados()
        self._seed_niveles_riesgo()
        self._seed_precios(servicios, rangos)

        self.stdout.write(self.style.SUCCESS("Seed de contenido de ejemplo completado."))

    def _seed_configuracion(self):
        if ConfiguracionSitio.objects.exists():
            self.stdout.write("ConfiguracionSitio ya existe, se omite.")
            return
        ConfiguracionSitio.objects.create(
            nombre_empresa="Consultores SST",
            eslogan="Gestión Humana y Seguridad en el Trabajo (contenido de ejemplo — edítalo en /admin)",
            mision=(
                "Acompañar a las empresas colombianas en la implementación de sistemas de "
                "gestión de seguridad y salud en el trabajo robustos y sostenibles. "
                "(Texto de ejemplo — edítalo en /admin)"
            ),
            vision=(
                "Ser la firma de referencia en consultoría SST y gestión humana en Colombia. "
                "(Texto de ejemplo — edítalo en /admin)"
            ),
            historia_titulo="Nuestra historia (ejemplo)",
            historia_texto=(
                "Consultores SST nació con el propósito de simplificar el cumplimiento normativo "
                "en seguridad y salud en el trabajo para empresas de todos los tamaños. "
                "(Texto de ejemplo — edítalo en /admin)"
            ),
            hero_titulo="Seguridad y Salud en el Trabajo, sin complicaciones (ejemplo)",
            hero_subtitulo="Cotiza en minutos los servicios SST que tu empresa necesita (contenido de ejemplo)",
            whatsapp_numero="573000000000",
            correo_contacto="contacto@ejemplo.com",
            telefono="6013000000",
            direccion="Calle 000 # 00-00, Bogotá (dirección de ejemplo)",
        )
        self.stdout.write(self.style.SUCCESS("ConfiguracionSitio creada."))

    def _seed_historia(self):
        hitos = [
            (2015, "Fundación", "Inicio de operaciones como consultora independiente de SST. (ejemplo)", 1),
            (2017, "Primeros 50 clientes", "Alcanzamos 50 empresas afiliadas a nuestros programas SST. (ejemplo)", 2),
            (2019, "Certificación ISO 9001", "Obtuvimos la certificación de calidad ISO 9001. (ejemplo)", 3),
            (2021, "Expansión regional", "Ampliamos cobertura a 5 departamentos adicionales. (ejemplo)", 4),
            (2024, "Plataforma digital", "Lanzamos nuestra plataforma digital de gestión documental SST. (ejemplo)", 5),
        ]
        for anio, titulo, descripcion, orden in hitos:
            HitoHistoria.objects.get_or_create(
                anio=anio,
                titulo=titulo,
                defaults={"descripcion": descripcion, "orden": orden},
            )
        self.stdout.write(self.style.SUCCESS("Hitos de historia creados."))

    def _seed_equipo(self):
        equipo = [
            {
                "nombre": "Nombre del Profesional — Ingeniero(a) SST",
                "cargo": "Ingeniero(a) SST Líder",
                "profesion": "Ingeniero Industrial",
                "tarjeta_profesional": "TP-000000",
                "bio": "Profesional con experiencia en implementación de SG-SST. (ejemplo)",
                "orden": 1,
            },
            {
                "nombre": "Nombre del Profesional — Abogado(a) Laboral",
                "cargo": "Abogado(a) Laboral",
                "profesion": "Abogado",
                "tarjeta_profesional": "TP-000001",
                "bio": "Asesoría jurídica en derecho laboral y riesgos laborales. (ejemplo)",
                "orden": 2,
            },
            {
                "nombre": "Nombre del Profesional — Administrador(a) de Empresas",
                "cargo": "Administrador(a) de Empresas",
                "profesion": "Administrador de Empresas",
                "tarjeta_profesional": "TP-000002",
                "bio": "Gestión administrativa y comercial de proyectos SST. (ejemplo)",
                "orden": 3,
            },
        ]
        for datos in equipo:
            MiembroEquipo.objects.get_or_create(nombre=datos["nombre"], defaults=datos)
        self.stdout.write(self.style.SUCCESS("Equipo de ejemplo creado."))

    def _seed_servicios(self):
        servicios_datos = [
            {
                "nombre": "SG-SST — Sistema de Gestión de Seguridad y Salud en el Trabajo",
                "slug": "sg-sst",
                "normativa": "Resolución 0312 de 2019",
                "descripcion_corta": (
                    "Diseño, implementación y mantenimiento del Sistema de Gestión de "
                    "Seguridad y Salud en el Trabajo."
                ),
                "descripcion_larga": (
                    "Acompañamiento integral para el diseño, implementación, ejecución y "
                    "mejora continua del SG-SST conforme a la Resolución 0312 de 2019. "
                    "(Contenido de ejemplo)"
                ),
                "destacado": True,
                "orden": 1,
            },
            {
                "nombre": "Plan Estratégico de Seguridad Vial (PESV)",
                "slug": "pesv",
                "normativa": "Resolución 40595",
                "descripcion_corta": "Diseño e implementación del Plan Estratégico de Seguridad Vial.",
                "descripcion_larga": (
                    "Formulación e implementación del PESV para empresas con flotas de "
                    "vehículos o personal que se desplaza por vías públicas. "
                    "(Contenido de ejemplo)"
                ),
                "destacado": True,
                "orden": 2,
            },
            {
                "nombre": "Trinorma ISO 45001 - 14001 - 9001",
                "slug": "trinorma-iso",
                "normativa": "",
                "descripcion_corta": "Implementación integrada de los sistemas de gestión ISO 45001, 14001 y 9001.",
                "descripcion_larga": (
                    "Implementación y auditoría de sistemas integrados de gestión de "
                    "calidad, ambiental y de seguridad y salud en el trabajo. "
                    "(Contenido de ejemplo)"
                ),
                "destacado": False,
                "orden": 3,
            },
            {
                "nombre": "Trabajo en Alturas y Espacios Confinados",
                "slug": "alturas-espacios-confinados",
                "normativa": "",
                "descripcion_corta": "Capacitación y certificación para trabajo seguro en alturas y espacios confinados.",
                "descripcion_larga": (
                    "Programas de formación, certificación y acompañamiento técnico para "
                    "trabajo seguro en alturas y en espacios confinados. "
                    "(Contenido de ejemplo)"
                ),
                "destacado": False,
                "orden": 4,
            },
            {
                "nombre": (
                    "Programas, Procedimientos y Capacitaciones "
                    "(SGA, SVE, Preoperacionales, Videos, Matrices)"
                ),
                "slug": "programas-procedimientos-capacitaciones",
                "normativa": "",
                "descripcion_corta": (
                    "Elaboración de programas, procedimientos, capacitaciones y matrices "
                    "requeridas por el SG-SST."
                ),
                "descripcion_larga": (
                    "Diseño de Sistemas de Gestión Ambiental (SGA), Sistemas de Vigilancia "
                    "Epidemiológica (SVE), exámenes preoperacionales, material audiovisual "
                    "y matrices de riesgo. (Contenido de ejemplo)"
                ),
                "destacado": False,
                "orden": 5,
            },
        ]
        servicios = []
        for datos in servicios_datos:
            servicio, _ = Servicio.objects.get_or_create(slug=datos["slug"], defaults=datos)
            servicios.append(servicio)
        self.stdout.write(self.style.SUCCESS("Servicios creados."))
        return servicios

    def _seed_clientes(self):
        # No se cargan logos de clientes de ejemplo porque requieren un archivo de
        # imagen real; se deja vacío a propósito, cárgalos desde /admin.
        self.stdout.write("LogoCliente: sin datos de ejemplo (requieren imagen), cárgalos desde /admin.")

    def _seed_rangos_empleados(self):
        rangos_datos = [
            {"nombre": "1 a 10 empleados", "empleados_min": 1, "empleados_max": 10, "orden": 1},
            {"nombre": "11 a 50 empleados", "empleados_min": 11, "empleados_max": 50, "orden": 2},
            {"nombre": "51 a 200 empleados", "empleados_min": 51, "empleados_max": 200, "orden": 3},
            {"nombre": "201 a 500 empleados", "empleados_min": 201, "empleados_max": 500, "orden": 4},
            {"nombre": "Más de 500 empleados", "empleados_min": 501, "empleados_max": None, "orden": 5},
        ]
        rangos = []
        for datos in rangos_datos:
            rango, _ = RangoEmpleados.objects.get_or_create(nombre=datos["nombre"], defaults=datos)
            rangos.append(rango)
        self.stdout.write(self.style.SUCCESS("Rangos de empleados creados."))
        return rangos

    def _seed_niveles_riesgo(self):
        niveles_datos = [
            {"nivel": NivelRiesgoARL.NIVEL_I, "nombre": "Riesgo I - Mínimo", "multiplicador": Decimal("1.00"), "orden": 1},
            {"nivel": NivelRiesgoARL.NIVEL_II, "nombre": "Riesgo II - Bajo", "multiplicador": Decimal("1.05"), "orden": 2},
            {"nivel": NivelRiesgoARL.NIVEL_III, "nombre": "Riesgo III - Medio", "multiplicador": Decimal("1.15"), "orden": 3},
            {"nivel": NivelRiesgoARL.NIVEL_IV, "nombre": "Riesgo IV - Alto", "multiplicador": Decimal("1.25"), "orden": 4},
            {"nivel": NivelRiesgoARL.NIVEL_V, "nombre": "Riesgo V - Máximo", "multiplicador": Decimal("1.40"), "orden": 5},
        ]
        for datos in niveles_datos:
            NivelRiesgoARL.objects.get_or_create(nivel=datos["nivel"], defaults=datos)
        self.stdout.write(self.style.SUCCESS("Niveles de riesgo ARL creados."))

    def _seed_precios(self, servicios, rangos):
        # Valores de ejemplo (placeholder) en pesos colombianos (COP), crecientes
        # con el tamaño de la empresa. Ajusta esta matriz a los precios reales del
        # negocio desde /admin (PrecioServicio es editable en línea en la lista).
        matriz = {
            "sg-sst": [450000, 900000, 2200000, 4500000, 8000000],
            "pesv": [300000, 650000, 1500000, 3200000, 6000000],
            "trinorma-iso": [600000, 1300000, 3000000, 6500000, 12000000],
            "alturas-espacios-confinados": [250000, 550000, 1200000, 2600000, 5000000],
            "programas-procedimientos-capacitaciones": [200000, 450000, 1000000, 2200000, 4200000],
        }
        creados = 0
        for servicio in servicios:
            precios_servicio = matriz.get(servicio.slug)
            if not precios_servicio:
                continue
            for rango, precio in zip(rangos, precios_servicio):
                _, created = PrecioServicio.objects.get_or_create(
                    servicio=servicio,
                    rango_empleados=rango,
                    defaults={"precio_base": Decimal(precio)},
                )
                creados += int(created)
        self.stdout.write(self.style.SUCCESS(f"Matriz de precios verificada/creada ({creados} nuevos registros)."))
