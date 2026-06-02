from rest_framework import serializers
from django.contrib.gis.geos import GEOSGeometry
from djangoapi.settings import EPSG_FOR_GEOMETRIES

from calidad_aire.models import (
    ZonaCalidadAire,
    CorredorEmision,
    EstacionMonitoreo
)


class WKTGeometryModelSerializer(serializers.ModelSerializer):
    """
    Serializer base para modelos con geometría.

    Su función es convertir la geometría del modelo Django/PostGIS
    a texto WKT cuando se envía al navegador o a Angular.

    También permite recibir geometrías en formato WKT cuando se
    haga una petición POST, PUT o PATCH desde Django REST Framework.
    """

    geom = serializers.CharField()

    def to_representation(self, instance):
        """
        Convierte el objeto Django en un diccionario serializable.

        En lugar de devolver la geometría como un objeto GEOS,
        la convierte a WKT, por ejemplo:

        POINT (1000500 1000500)
        LINESTRING (1000100 1000100, 1000200 1000200)
        POLYGON ((...))
        """

        data = super().to_representation(instance)

        if instance.geom:
            data["geom"] = instance.geom.wkt
        else:
            data["geom"] = None

        return data

    def validate_geom(self, value):
        """
        Valida la geometría recibida desde la API REST.

        Recibe un texto WKT, lo convierte a GEOSGeometry y verifica
        que sea una geometría válida.
        """

        try:
            geom = GEOSGeometry(value, srid=EPSG_FOR_GEOMETRIES)
        except Exception:
            raise serializers.ValidationError("Invalid WKT geometry")

        if not geom.valid:
            raise serializers.ValidationError("Invalid geometry")

        return geom


class ZonaCalidadAireSerializer(WKTGeometryModelSerializer):
    """
    Serializer para la tabla poligonal calidad_aire.zona_calidad_aire.
    """

    class Meta:
        model = ZonaCalidadAire
        fields = "__all__"


class CorredorEmisionSerializer(WKTGeometryModelSerializer):
    """
    Serializer para la tabla lineal calidad_aire.corredor_emision.
    """

    class Meta:
        model = CorredorEmision
        fields = "__all__"


class EstacionMonitoreoSerializer(WKTGeometryModelSerializer):
    """
    Serializer para la tabla puntual calidad_aire.estacion_monitoreo.
    """

    class Meta:
        model = EstacionMonitoreo
        fields = "__all__"
