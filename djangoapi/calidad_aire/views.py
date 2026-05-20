from django.http import JsonResponse
from django.contrib.gis.geos import GEOSGeometry

from rest_framework import serializers
from rest_framework import viewsets
from rest_framework import permissions

from core.myLib.baseDjangoView import BaseDjangoView

from calidad_aire.models import (
    ZonaCalidadAire,
    CorredorEmision,
    EstacionMonitoreo
)

from scripts.p1.django_models.zona_calidad_aire_django import ZonaCalidadAireDjango
from scripts.p1.django_models.corredor_emision_django import CorredorEmisionDjango
from scripts.p1.django_models.estacion_monitoreo_django import EstacionMonitoreoDjango


EPSG_CODE = 9377


# =========================================================
# RESPUESTAS COMUNES PARA AUTENTICACIÓN
# =========================================================

def not_authenticated_response():
    return JsonResponse({
        "ok": False,
        "message": "User is not authenticated",
        "data": []
    })


def user_is_not_authenticated(request):
    return not request.user.is_authenticated


# =========================================================
# SERIALIZERS PARA DJANGO REST FRAMEWORK
# Estos serializers permiten que la geometría se vea como WKT
# en la API navegable de Django REST Framework.
# =========================================================

class WKTGeometryModelSerializer(serializers.ModelSerializer):
    geom = serializers.CharField()

    def to_representation(self, instance):
        data = super().to_representation(instance)

        if instance.geom:
            data["geom"] = instance.geom.wkt
        else:
            data["geom"] = None

        return data

    def validate_geom(self, value):
        try:
            geom = GEOSGeometry(value, srid=EPSG_CODE)
        except Exception:
            raise serializers.ValidationError("Invalid WKT geometry")

        if not geom.valid:
            raise serializers.ValidationError("Invalid geometry")

        return geom


class ZonaCalidadAireSerializer(WKTGeometryModelSerializer):

    class Meta:
        model = ZonaCalidadAire
        fields = "__all__"


class CorredorEmisionSerializer(WKTGeometryModelSerializer):

    class Meta:
        model = CorredorEmision
        fields = "__all__"


class EstacionMonitoreoSerializer(WKTGeometryModelSerializer):

    class Meta:
        model = EstacionMonitoreo
        fields = "__all__"


# =========================================================
# VIEWS CON BASEDJANGOVIEW
# Estas son las vistas principales del taller.
# Se usan con rutas tipo:
# /calidad_aire/estacion_monitoreo/selectall/
# /calidad_aire/estacion_monitoreo/insert/
# /calidad_aire/estacion_monitoreo/update/1/
# /calidad_aire/estacion_monitoreo/delete/1/
# =========================================================

class ZonaCalidadAireView(BaseDjangoView):

    def insert(self, request):
        if user_is_not_authenticated(request):
            return not_authenticated_response()

        d = request.POST.dict()
        zona = ZonaCalidadAireDjango()
        result = zona.insert(d)
        return JsonResponse(result)

    def selectone(self, id):
        zona = ZonaCalidadAireDjango()
        result = zona.selectAsDicts({"id": id})
        return JsonResponse(result)

    def selectall(self):
        zona = ZonaCalidadAireDjango()
        result = zona.selectAllAsDicts()
        return JsonResponse(result)

    def update(self, request, id):
        if user_is_not_authenticated(request):
            return not_authenticated_response()

        d = request.POST.dict()
        d["id"] = id
        zona = ZonaCalidadAireDjango()
        result = zona.update(d)
        return JsonResponse(result)

    def delete(self, id):
        if user_is_not_authenticated(self.request):
            return not_authenticated_response()

        zona = ZonaCalidadAireDjango()
        result = zona.delete({"id": id})
        return JsonResponse(result)


class CorredorEmisionView(BaseDjangoView):

    def insert(self, request):
        if user_is_not_authenticated(request):
            return not_authenticated_response()

        d = request.POST.dict()
        corredor = CorredorEmisionDjango()
        result = corredor.insert(d)
        return JsonResponse(result)

    def selectone(self, id):
        corredor = CorredorEmisionDjango()
        result = corredor.selectAsDicts({"id": id})
        return JsonResponse(result)

    def selectall(self):
        corredor = CorredorEmisionDjango()
        result = corredor.selectAllAsDicts()
        return JsonResponse(result)

    def update(self, request, id):
        if user_is_not_authenticated(request):
            return not_authenticated_response()

        d = request.POST.dict()
        d["id"] = id
        corredor = CorredorEmisionDjango()
        result = corredor.update(d)
        return JsonResponse(result)

    def delete(self, id):
        if user_is_not_authenticated(self.request):
            return not_authenticated_response()

        corredor = CorredorEmisionDjango()
        result = corredor.delete({"id": id})
        return JsonResponse(result)


class EstacionMonitoreoView(BaseDjangoView):

    def insert(self, request):
        if user_is_not_authenticated(request):
            return not_authenticated_response()

        d = request.POST.dict()
        estacion = EstacionMonitoreoDjango()
        result = estacion.insert(d)
        return JsonResponse(result)

    def selectone(self, id):
        estacion = EstacionMonitoreoDjango()
        result = estacion.selectAsDicts({"id": id})
        return JsonResponse(result)

    def selectall(self):
        estacion = EstacionMonitoreoDjango()
        result = estacion.selectAllAsDicts()
        return JsonResponse(result)

    def update(self, request, id):
        if user_is_not_authenticated(request):
            return not_authenticated_response()

        d = request.POST.dict()
        d["id"] = id
        estacion = EstacionMonitoreoDjango()
        result = estacion.update(d)
        return JsonResponse(result)

    def delete(self, id):
        if user_is_not_authenticated(self.request):
            return not_authenticated_response()

        estacion = EstacionMonitoreoDjango()
        result = estacion.delete({"id": id})
        return JsonResponse(result)


# =========================================================
# VIEWS DE DJANGO REST FRAMEWORK
# Estas clases permiten ver la API Root en:
# http://localhost:8002/calidad_aire/
#
# No reemplazan las vistas anteriores.
# Solo agregan una interfaz navegable parecida a la del profesor.
# =========================================================

class ZonaCalidadAireModelViewSet(viewsets.ModelViewSet):
    queryset = ZonaCalidadAire.objects.all().order_by("id")
    serializer_class = ZonaCalidadAireSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class CorredorEmisionModelViewSet(viewsets.ModelViewSet):
    queryset = CorredorEmision.objects.all().order_by("id")
    serializer_class = CorredorEmisionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class EstacionMonitoreoModelViewSet(viewsets.ModelViewSet):
    queryset = EstacionMonitoreo.objects.all().order_by("id")
    serializer_class = EstacionMonitoreoSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]