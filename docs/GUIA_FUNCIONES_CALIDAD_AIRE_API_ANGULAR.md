# Guia funciones calidad aire API Angular

## 1. Introduccion

`calidad-aire-api` es el backend Django/PostGIS del geoportal. Mantiene la estructura del profesor: apps Django, modelos en `models.py`, vistas basadas en `BaseDjangoView`, rutas por accion y respuestas JSON con la forma:

```json
{"ok": true, "message": "mensaje", "data": []}
```

`calidad-aire-angular` es el frontend Angular/OpenLayers. Consume la API mediante `SettingsService` y `ApiService`, muestra mapa OpenLayers, dibuja geometria WKT y trabaja con formularios reactivos.

URLs de produccion esperadas:

- Web: `https://buitrago.geomaticaupv.es`
- API por Apache proxy: `https://buitrago.geomaticaupv.es/api/`
- Django interno en Docker: `127.0.0.1:8006`
- GeoServer por proxy: `https://buitrago.geomaticaupv.es/geoserver/`

El diseno visual del frontend se conserva. El unico ajuste visual indirecto fue la configuracion de URLs de servicios; no se cambiaron colores, layout, componentes ni estilos globales para examen 1 y 2.

## 2. Examen 1: virtualhost, SSL, sitio y proxy

La plantilla Apache queda en `docs/apache-buitrago.geomaticaupv.es.conf`.

Pasos en VPS:

```bash
sudo cp docs/apache-buitrago.geomaticaupv.es.conf /etc/apache2/sites-available/buitrago.geomaticaupv.es.conf
sudo mkdir -p /var/www/html/buitrago.geomaticaupv.es
sudo chown -R buitrago:www-data /var/www/html/buitrago.geomaticaupv.es
sudo a2ensite buitrago.geomaticaupv.es.conf
sudo apachectl configtest
sudo systemctl restart apache2
sudo certbot --apache -d buitrago.geomaticaupv.es
```

Antes de reiniciar Apache siempre debe salir `Syntax OK` en `sudo apachectl configtest`.

Proxy configurado:

- `/api/` apunta a `http://127.0.0.1:8006/`.
- `/geoserver/` apunta a `http://127.0.0.1:7006/geoserver/`.

## 3. Examen 2: Django API en Docker produccion

Archivos principales:

- `docker-compose.prod.yml`: deja activo solo `djangoapi`, usa Gunicorn y publica `127.0.0.1:8006:8000`.
- `.env.prod.example`: plantilla sin secretos para crear `.env.prod` en el VPS.
- `.env`: fija los puertos asignados a Buitrago: PostGIS `5006`, GeoServer `7006`, Django API `8006`, PgAdmin `9006`.
- `djangoapi/djangoapi/settings.py`: lee `DJANGO_ALLOWED_HOSTS`, `CORS_ALLOWED_ORIGINS`, `DJANGO_CSRF_TRUSTED_ORIGINS`, `FORCE_SCRIPT_NAME`, `STATIC_ROOT` y `STATIC_URL`.

Comandos en VPS:

```bash
cd /home/buitrago/docker/calidad-aire-api
cp .env.prod.example .env.prod
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
docker compose -f docker-compose.prod.yml up
docker compose -f docker-compose.prod.yml up -d
docker compose -f docker-compose.prod.yml exec djangoapi python manage.py migrate
docker compose -f docker-compose.prod.yml exec djangoapi python manage.py collectstatic
```

La red Docker productiva configurada es externa:

```yaml
joamona-dj-api_postgis:
  external: true
```

## 4. Estructura backend

Proyecto Django: `djangoapi`.

App de calidad de aire: `djangoapi/calidad_aire`.

Modelos:

- `ZonaCalidadAire`: tabla `calidad_aire.zona_calidad_aire`, `PolygonField`, SRID `9377`.
- `CorredorEmision`: tabla `calidad_aire.corredor_emision`, `LineStringField`, SRID `9377`.
- `EstacionMonitoreo`: tabla `calidad_aire.estacion_monitoreo`, `PointField`, SRID `9377`.

Vistas:

- `ZonaCalidadAireView`
- `CorredorEmisionView`
- `EstacionMonitoreoView`

Clases de logica:

- `scripts/p1/django_models/zona_calidad_aire_django.py`
- `scripts/p1/django_models/corredor_emision_django.py`
- `scripts/p1/django_models/estacion_monitoreo_django.py`

## 5. Tabla endpoints backend

| Entidad | Endpoint | Metodo | Funcion |
|---|---|---:|---|
| Zona | `/calidad_aire/zona_calidad_aire/selectall/` | GET | `ZonaCalidadAireView.selectall` |
| Zona | `/calidad_aire/zona_calidad_aire/selectone/<id>/` | GET | `ZonaCalidadAireView.selectone` |
| Zona | `/calidad_aire/zona_calidad_aire/insert/` | POST | `ZonaCalidadAireView.insert` |
| Zona | `/calidad_aire/zona_calidad_aire/update/<id>/` | POST | `ZonaCalidadAireView.update` |
| Zona | `/calidad_aire/zona_calidad_aire/delete/<id>/` | POST | `ZonaCalidadAireView.delete` |
| Corredor | `/calidad_aire/corredor_emision/selectall/` | GET | `CorredorEmisionView.selectall` |
| Corredor | `/calidad_aire/corredor_emision/selectone/<id>/` | GET | `CorredorEmisionView.selectone` |
| Corredor | `/calidad_aire/corredor_emision/insert/` | POST | `CorredorEmisionView.insert` |
| Corredor | `/calidad_aire/corredor_emision/update/<id>/` | POST | `CorredorEmisionView.update` |
| Corredor | `/calidad_aire/corredor_emision/delete/<id>/` | POST | `CorredorEmisionView.delete` |
| Estacion | `/calidad_aire/estacion_monitoreo/selectall/` | GET | `EstacionMonitoreoView.selectall` |
| Estacion | `/calidad_aire/estacion_monitoreo/selectone/<id>/` | GET | `EstacionMonitoreoView.selectone` |
| Estacion | `/calidad_aire/estacion_monitoreo/insert/` | POST | `EstacionMonitoreoView.insert` |
| Estacion | `/calidad_aire/estacion_monitoreo/update/<id>/` | POST | `EstacionMonitoreoView.update` |
| Estacion | `/calidad_aire/estacion_monitoreo/delete/<id>/` | POST | `EstacionMonitoreoView.delete` |

En produccion se consumen con prefijo Apache:

```text
https://buitrago.geomaticaupv.es/api/calidad_aire/estacion_monitoreo/selectall/
```

## 6. Funcion por funcion backend

### ZonaCalidadAireDjango.insert

Archivo: `scripts/p1/django_models/zona_calidad_aire_django.py`.

Entrada: `codigo_zona`, `nombre_zona`, `municipio`, `geom` y campos opcionales de contaminantes.

Validaciones:

- Campos obligatorios.
- Contaminantes no negativos.
- Geometria valida con `ST_IsValid(ST_SnapToGrid(..., 0.0001))`.
- Poligono sin interseccion interior con otro poligono mediante `ST_Relate(..., 'T********')`.

Calcula `area_ha` con `geom.area / 10000`, guarda el modelo y devuelve el `id`.

### ZonaCalidadAireDjango.update

Recibe `id` por URL y datos del formulario. Verifica existencia, repite validaciones excluyendo el mismo `id`, recalcula `area_ha` y devuelve `rows_updated`.

### ZonaCalidadAireDjango.delete

Recibe `id`, verifica existencia, elimina el registro y devuelve `rows_deleted`.

### ZonaCalidadAireDjango.selectAsDicts

Recibe `id`, devuelve un registro con `geom` en WKT y fecha en formato `YYYY-MM-DD`.

### ZonaCalidadAireDjango.selectAllAsDicts

Devuelve todos los poligonos ordenados por `id`, con `geom` en WKT para OpenLayers.

### CorredorEmisionDjango.insert

Entrada: `codigo_corredor`, `nombre_corredor`, `municipio`, `geom` y campos opcionales de via/emision.

Validaciones:

- Campos obligatorios.
- Contaminantes estimados no negativos.
- Geometria valida con `ST_SnapToGrid`.
- La linea no intersecta otra linea existente con `ST_Intersects`.

Calcula `longitud_km` con `geom.length / 1000`.

### CorredorEmisionDjango.update

Verifica `id`, existencia y validaciones topologicas excluyendo el registro actual. Actualiza campos y recalcula `longitud_km`.

### CorredorEmisionDjango.delete

Elimina el corredor si existe y devuelve `rows_deleted`.

### CorredorEmisionDjango.selectAsDicts

Devuelve un corredor por `id` con geometria WKT.

### CorredorEmisionDjango.selectAllAsDicts

Devuelve todos los corredores ordenados por `id`.

### EstacionMonitoreoDjango.insert

Entrada: `codigo_estacion`, `nombre_estacion`, `municipio`, `geom` y contaminantes.

Validaciones:

- Campos obligatorios.
- Contaminantes no negativos.
- Punto valido con `ST_SnapToGrid`.
- Punto dentro de una zona con `ST_Within`.

Guarda el punto y devuelve el `id`.

### EstacionMonitoreoDjango.update

Verifica `id`, existencia, datos obligatorios, contaminantes, geometria valida y punto dentro de una zona. Actualiza campos y devuelve `rows_updated`.

### EstacionMonitoreoDjango.delete

Elimina la estacion si existe y devuelve `rows_deleted`.

### EstacionMonitoreoDjango.selectAsDicts

Devuelve una estacion por `id`, con `geom` en WKT y `fecha_medicion` como texto.

### EstacionMonitoreoDjango.selectAllAsDicts

Devuelve todas las estaciones ordenadas por `id`.

## 7. Parametrizacion backend

Para adaptar `estacion_monitoreo` a sensores:

- Cambiar modelo `EstacionMonitoreo` por `Sensor`.
- Cambiar tabla `calidad_aire.estacion_monitoreo` por la tabla nueva.
- Mantener `PointField(srid=9377)` si sigue siendo punto.
- Cambiar campos obligatorios y endpoint a `/sensores/insert/`.
- Mantener respuesta `ok`, `message`, `data`.

Para adaptar `zona_calidad_aire` a parcelas:

- Cambiar modelo `ZonaCalidadAire` por `Parcela`.
- Mantener `PolygonField` si son poligonos.
- Mantener `ST_Relate(..., 'T********')` si se quiere evitar solape interior.
- Cambiar campos descriptivos y endpoint.

## 8. Estructura frontend

Servicios:

- `SettingsService`: centraliza URL de API y GeoServer. En local usa `http://localhost:8001/`; en produccion usa `https://buitrago.geomaticaupv.es/api/`.
- `ApiService`: centraliza `get` y `post` con `withCredentials`.
- `MapService`: crea mapa, capas WMS, capas vectoriales, lee WKT desde `selectall` y lo agrega al mapa.
- `AuthService`: comprueba login y usuario.
- `EventService`: comunica dibujo y formularios.

Componentes principales:

- `MapComponent`
- `DrawZonaCalidadAireComponent`
- `DrawCorredorEmisionComponent`
- `DrawEstacionMonitoreoComponent`
- Formularios de zona, corredor, estacion, login y logout.

## 9. Funciones frontend clave

`ApiService.get(endpoint)`: llama `SettingsService.API_URL + endpoint`, espera `ServerAnswerModel`.

`ApiService.post(endpoint, data)`: transforma objeto a `application/x-www-form-urlencoded` y envia POST.

`MapService.loadAllGeometriesInMap()`: carga zonas, corredores y estaciones.

`MapService.addWktListToVectorLayer(data, layerTitle, tableName)`: convierte WKT a `Feature` en `EPSG:9377`.

`SettingsService.getApiUrl()`: selecciona API local o API publicada.

`SettingsService.getGeoserverUrl()`: selecciona GeoServer local o proxy publicado.

Para reutilizar frontend con otra API:

- Cambiar `SettingsService.API_URL`.
- Cambiar endpoints enviados desde formularios y `MapService`.
- Crear modelos TypeScript con los campos nuevos.
- Cambiar `FormGroup` y validaciones.
- Cambiar tipo de dibujo OpenLayers segun `Point`, `LineString` o `Polygon`.

## 10. Pruebas

API local:

```bash
curl http://127.0.0.1:8006/
curl http://127.0.0.1:8006/core/hello_world/
curl http://127.0.0.1:8006/calidad_aire/zona_calidad_aire/selectall/
```

API por proxy:

```bash
curl https://buitrago.geomaticaupv.es/api/
curl https://buitrago.geomaticaupv.es/api/core/hello_world/
curl https://buitrago.geomaticaupv.es/api/calidad_aire/estacion_monitoreo/selectall/
```

Apache:

```bash
sudo apachectl configtest
sudo systemctl restart apache2
```

Docker:

```bash
docker ps
docker compose -f docker-compose.prod.yml logs djangoapi
```

Angular:

```bash
npm install
npm run build
```

## 11. Como explicar este proyecto al profesor

El geoportal gestiona calidad del aire con tres capas espaciales: zonas, corredores y estaciones. Angular usa `SettingsService` para conocer la URL base, `ApiService` para peticiones y `MapService` para pintar WKT en OpenLayers. Apache publica la web como sitio estatico y redirige `/api/` hacia Django en Docker. Docker ejecuta Django con Gunicorn en el puerto interno 8000 y lo expone solo en `127.0.0.1:8006`. PostGIS almacena las geometrías en SRID `9377`. La estructura se mantiene como en clase: modelos, vistas `BaseDjangoView`, rutas por accion y respuestas `ok/message/data`.

## 12. Pendientes reales

- Copiar `.env.prod.example` a `.env.prod` en el VPS y completar secretos reales.
- Ejecutar los comandos SSH, Apache, Docker y Certbot en el servidor con la contraseña del usuario `buitrago`.
- Publicar las capas WMS en GeoServer si todavia no estan creadas en el servidor.
