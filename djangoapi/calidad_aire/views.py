from django.http import JsonResponse

from core.myLib.baseDjangoView import BaseDjangoView

from scripts.p1.django_models.zona_calidad_aire_django import ZonaCalidadAireDjango
from scripts.p1.django_models.corredor_emision_django import CorredorEmisionDjango
from scripts.p1.django_models.estacion_monitoreo_django import EstacionMonitoreoDjango


def not_authenticated_response():
    return JsonResponse({
        "ok": False,
        "message": "User is not authenticated",
        "data": []
    })


def user_is_not_authenticated(request):
    return not request.user.is_authenticated


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