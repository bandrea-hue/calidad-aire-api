from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin

from rest_framework import viewsets
from rest_framework import permissions

from core.myLib.baseDjangoView import BaseDjangoView

from calidad_aire.models import (
    ZonaCalidadAire,
    CorredorEmision,
    EstacionMonitoreo
)
from calidad_aire.serializers import (
    ZonaCalidadAireSerializer,
    CorredorEmisionSerializer,
    EstacionMonitoreoSerializer
)

from scripts.p1.django_models.zona_calidad_aire_django import ZonaCalidadAireDjango
from scripts.p1.django_models.corredor_emision_django import CorredorEmisionDjango
from scripts.p1.django_models.estacion_monitoreo_django import EstacionMonitoreoDjango


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
# VIEWS CON BASEDJANGOVIEW
# Estas son las vistas principales del taller.
# Se usan con rutas tipo:
# /calidad_aire/estacion_monitoreo/selectall/
# /calidad_aire/estacion_monitoreo/insert/
# /calidad_aire/estacion_monitoreo/update/1/
# /calidad_aire/estacion_monitoreo/delete/1/
# =========================================================

class ZonaCalidadAireView(LoginRequiredMixin, BaseDjangoView):

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


class CorredorEmisionView(LoginRequiredMixin, BaseDjangoView):

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


class EstacionMonitoreoView(LoginRequiredMixin, BaseDjangoView):

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
