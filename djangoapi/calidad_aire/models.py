from django.db import models
from django.contrib.gis.db import models as gis_models


class ZonaCalidadAire(models.Model):
    codigo_zona = models.CharField(max_length=50, unique=True)
    nombre_zona = models.CharField(max_length=150)
    municipio = models.CharField(max_length=100)
    poblacion = models.IntegerField(blank=True, null=True)
    area_ha = models.FloatField(blank=True, null=True)
    pm25_promedio = models.FloatField(blank=True, null=True)
    pm10_promedio = models.FloatField(blank=True, null=True)
    no2_promedio = models.FloatField(blank=True, null=True)
    indice_calidad_aire = models.IntegerField(blank=True, null=True)
    categoria_ica = models.CharField(max_length=50, blank=True, null=True)
    fecha_actualizacion = models.DateField(blank=True, null=True)
    geom = gis_models.PolygonField(srid=9377)

    class Meta:
        managed = False
        db_table = '"calidad_aire"."zona_calidad_aire"'


class CorredorEmision(models.Model):
    codigo_corredor = models.CharField(max_length=50, unique=True)
    nombre_corredor = models.CharField(max_length=150)
    municipio = models.CharField(max_length=100)
    tipo_via = models.CharField(max_length=80, blank=True, null=True)
    fuente_emision = models.CharField(max_length=100, blank=True, null=True)
    flujo_vehicular = models.IntegerField(blank=True, null=True)
    velocidad_promedio = models.FloatField(blank=True, null=True)
    pm25_estimado = models.FloatField(blank=True, null=True)
    no2_estimado = models.FloatField(blank=True, null=True)
    categoria_emision = models.CharField(max_length=50, blank=True, null=True)
    longitud_km = models.FloatField(blank=True, null=True)
    fecha_actualizacion = models.DateField(blank=True, null=True)
    geom = gis_models.LineStringField(srid=9377)

    class Meta:
        managed = False
        db_table = '"calidad_aire"."corredor_emision"'


class EstacionMonitoreo(models.Model):
    codigo_estacion = models.CharField(max_length=50, unique=True)
    nombre_estacion = models.CharField(max_length=150)
    municipio = models.CharField(max_length=100)
    tipo_estacion = models.CharField(max_length=80, blank=True, null=True)
    responsable = models.CharField(max_length=120, blank=True, null=True)
    pm25 = models.FloatField(blank=True, null=True)
    pm10 = models.FloatField(blank=True, null=True)
    no2 = models.FloatField(blank=True, null=True)
    o3 = models.FloatField(blank=True, null=True)
    co = models.FloatField(blank=True, null=True)
    indice_calidad_aire = models.IntegerField(blank=True, null=True)
    categoria_ica = models.CharField(max_length=50, blank=True, null=True)
    fecha_medicion = models.DateField(blank=True, null=True)
    estado = models.CharField(max_length=30, default="Activa")
    geom = gis_models.PointField(srid=9377)

    class Meta:
        managed = False
        db_table = '"calidad_aire"."estacion_monitoreo"'