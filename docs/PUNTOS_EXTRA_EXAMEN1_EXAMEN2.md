# Puntos extra examen 1 y examen 2

## Resumen

Segun la guia `00-gestcont2026_en.pdf`, los puntos extra relacionados con examen 1 y examen 2 son:

| Examen | Seccion guia | Valor | Estado |
|---|---:|---:|---|
| Examen 1 | 2.12 Exercise 1: virtualhosts, SSL, publish a site, and create proxy in the VPS | 0.5 puntos | Implementado |
| Examen 2 | 3.10 Exercise 2: Publish your Docker Django API in a production server | 1 punto | Implementado |

## Examen 1: Exercise 1

La guia pide:

- Crear usuario propio en VPS.
- Crear virtualhost `buitrago.geomaticaupv.es`.
- Configurar `ServerName`.
- Configurar `DocumentRoot`.
- Publicar un sitio en `/var/www/html/buitrago`.
- Activar SSL con Certbot.
- Crear proxy Apache para Fiware.
- Usar puertos del estudiante Buitrago, numero `06`.
- Probar `https://buitrago.geomaticaupv.es` y `https://buitrago.geomaticaupv.es/fiware/version/`.

Estado en servidor:

- Sitio publico: `https://buitrago.geomaticaupv.es`
- DocumentRoot: `/var/www/html/buitrago`
- Apache SSL: activo.
- Proxy `/fiware/`: activo.
- Orion Fiware: `127.0.0.1:7006 -> 1026`
- Mongo Fiware: `127.0.0.1:9006 -> 27017`
- Contenedores:
  - `buitrago-fiware-orion`
  - `buitrago-db-mongo`

Prueba realizada:

```bash
curl https://buitrago.geomaticaupv.es/fiware/version/
```

Resultado esperado:

```json
{
  "orion": {
    "version": "4.0.0"
  }
}
```

## Examen 2: Exercise 2

La guia pide:

- Usar git y tener API clonada en `/home/buitrago/docker`.
- Configurar `.env.prod`.
- Configurar `DEBUG=False`.
- Configurar `SECRET_KEY` de produccion.
- Configurar `DJANGO_ALLOWED_HOSTS`.
- Configurar `CORS_ALLOWED_ORIGINS`.
- Configurar `DJANGO_CSRF_TRUSTED_ORIGINS`.
- Usar `docker-compose.prod.yml`.
- Publicar API por Apache con `/api/`.
- Hacer funcionar Django Admin.
- Ejecutar `collectstatic`.
- Publicar capas WMS desde GeoServer.
- Usar las capas WMS desde QGIS o cliente WMS.

Estado en servidor:

- API en Docker: `buitrago-api-djangoapi-1`
- Puerto API: `127.0.0.1:8006 -> 8000`
- URL API: `https://buitrago.geomaticaupv.es/api/`
- Endpoint probado: `https://buitrago.geomaticaupv.es/api/core/hello_world/`
- Base PostGIS: `buitrago`
- Esquema: `calidad_aire`
- Tablas espaciales:
  - `zona_calidad_aire`
  - `corredor_emision`
  - `estacion_monitoreo`
- Django admin con estaticos: `collectstatic` ejecutado y archivos copiados a `/var/www/html/buitrago/static_root`.

Prueba API:

```bash
curl https://buitrago.geomaticaupv.es/api/core/hello_world/
```

Resultado:

```json
{"ok": true, "message": "Core. Hello world", "data": []}
```

Prueba CRUD realizada por HTTPS:

- `insert`, `selectone`, `update`, `delete` de `zona_calidad_aire`.
- `insert`, `update`, `delete` de `corredor_emision`.
- `insert`, `update`, `delete` de `estacion_monitoreo`.

## WMS publicados en GeoServer

Workspace:

```text
calidad_aire
```

Datastore:

```text
buitrago_postgis
```

Capas publicadas:

```text
calidad_aire:zona_calidad_aire
calidad_aire:corredor_emision
calidad_aire:estacion_monitoreo
```

GetCapabilities:

```bash
curl "https://buitrago.geomaticaupv.es/geoserver/calidad_aire/wms?service=WMS&request=GetCapabilities"
```

GetMap de prueba:

```bash
curl -o zona_wms.png "https://buitrago.geomaticaupv.es/geoserver/calidad_aire/wms?service=WMS&version=1.1.0&request=GetMap&layers=calidad_aire:zona_calidad_aire&bbox=4999000,1999000,5002000,2002000&width=512&height=512&srs=EPSG:9377&styles=&format=image/png&transparent=true"
```

Resultado verificado:

```text
HTTP 200
Content-Type: image/png
PNG image data, 512 x 512
```

## Ajuste tecnico adicional

Para que GeoServer pudiera publicar y renderizar capas en `EPSG:9377`, se registro la proyeccion:

- En GeoServer: `user_projections/epsg.properties`.
- En PostGIS: tabla `spatial_ref_sys`, `srid=9377`.

Esto fue necesario porque GeoServer inicialmente devolvia:

```text
This is unexpected, the layer srs seems to be mis-configured
```

y luego WMS indicaba:

```text
Cannot find SRID (9377) in spatial_ref_sys
```

Despues del ajuste, WMS devuelve imagen PNG correctamente.

## URLs para mostrar al profesor

```text
https://buitrago.geomaticaupv.es
https://buitrago.geomaticaupv.es/fiware/version/
https://buitrago.geomaticaupv.es/api/core/hello_world/
https://buitrago.geomaticaupv.es/api/admin/
https://buitrago.geomaticaupv.es/geoserver/
https://buitrago.geomaticaupv.es/geoserver/calidad_aire/wms?service=WMS&request=GetCapabilities
```

## Pendiente no tecnico

La guia pide subir un PDF con evidencias al aula o carpeta compartida. Este archivo contiene la evidencia textual; para la entrega formal se puede exportar a PDF y anadir capturas si el profesor las exige.
