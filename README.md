# SST Landing API

Backend Django + DRF para la landing page de una empresa de Gestión Humana y
Seguridad y Salud en el Trabajo (SST), con cotizador de servicios en tiempo real.

## Arranque rápido

```bash
cp .env.example .env   # ya viene copiado como .env en este repo; ajusta valores si hace falta
docker compose up -d --build
```

Esto levanta Postgres (`db`) y la API (`api`) en `http://localhost:8095/`.
Con `SEED_DEMO=true` en `.env`, al iniciar el contenedor `api` se carga
automáticamente contenido de ejemplo (empresa, equipo, servicios, precios).

## Crear superusuario

```bash
docker compose exec api python manage.py createsuperuser
```

Luego entra a `http://localhost:8095/admin/`.

## Endpoints principales

```
GET  /api/config/
GET  /api/historia/
GET  /api/equipo/
GET  /api/servicios/
GET  /api/clientes/
GET  /api/cotizador/rangos-empleados/
GET  /api/cotizador/niveles-riesgo/
POST /api/cotizador/calcular/
POST /api/cotizador/solicitudes/
POST /api/contacto/mensajes/
```

## IMPORTANTE — contenido de ejemplo

Todo el contenido cargado por `seed_demo_content` (nombre de la empresa, eslogan,
misión/visión, historia, equipo, textos de servicios y la matriz de precios) es
**contenido de ejemplo (placeholder)**. Antes de publicar el sitio real, edita
todo desde `/admin/`:

- `ConfiguracionSitio`: nombre real de la empresa, logo, WhatsApp, correo, redes.
- `MiembroEquipo`: nombres, cargos y fotos reales del equipo.
- `Servicio`: textos descriptivos ajustados a la oferta real (los 5 servicios y
  su normativa ya son los reales del dominio SST, no hace falta cambiarlos).
- `PrecioServicio`: la matriz de precios (servicio × rango de empleados) trae
  valores de ejemplo en COP — deben ajustarse a los precios reales del negocio.
- `LogoCliente`: no trae datos de ejemplo (requiere imágenes reales), cárgalos
  directamente desde `/admin/`.
