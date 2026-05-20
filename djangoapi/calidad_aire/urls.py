from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views


app_name = "calidad_aire"


# =========================================================
# ROUTER DE DJANGO REST FRAMEWORK
# Este router permite que la ruta:
# http://localhost:8002/calidad_aire/
# muestre una API Root similar a la del profesor.
# =========================================================

router = DefaultRouter()

router.register(
    r"zonas",
    views.ZonaCalidadAireModelViewSet,
    basename="zonas"
)

router.register(
    r"corredores",
    views.CorredorEmisionModelViewSet,
    basename="corredores"
)

router.register(
    r"estaciones",
    views.EstacionMonitoreoModelViewSet,
    basename="estaciones"
)


urlpatterns = [
    # ---------------------------------------------------------
    # Rutas Django REST Framework
    # Permiten ver una API Root en:
    # http://localhost:8002/calidad_aire/
    #
    # Y acceder a:
    # http://localhost:8002/calidad_aire/zonas/
    # http://localhost:8002/calidad_aire/corredores/
    # http://localhost:8002/calidad_aire/estaciones/
    # ---------------------------------------------------------
    path("", include(router.urls)),

    # ---------------------------------------------------------
    # Rutas propias del taller usando BaseDjangoView
    # Estas son las rutas que usaremos desde Angular.
    # ---------------------------------------------------------

    # Tabla poligonal: zona_calidad_aire
    path(
        "zona_calidad_aire/<str:action>/",
        views.ZonaCalidadAireView.as_view(),
        name="zona_calidad_aire_action"
    ),
    path(
        "zona_calidad_aire/<str:action>/<int:id>/",
        views.ZonaCalidadAireView.as_view(),
        name="zona_calidad_aire_action_id"
    ),

    # Tabla lineal: corredor_emision
    path(
        "corredor_emision/<str:action>/",
        views.CorredorEmisionView.as_view(),
        name="corredor_emision_action"
    ),
    path(
        "corredor_emision/<str:action>/<int:id>/",
        views.CorredorEmisionView.as_view(),
        name="corredor_emision_action_id"
    ),

    # Tabla puntual: estacion_monitoreo
    path(
        "estacion_monitoreo/<str:action>/",
        views.EstacionMonitoreoView.as_view(),
        name="estacion_monitoreo_action"
    ),
    path(
        "estacion_monitoreo/<str:action>/<int:id>/",
        views.EstacionMonitoreoView.as_view(),
        name="estacion_monitoreo_action_id"
    ),
]