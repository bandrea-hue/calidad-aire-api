from django.urls import path
from . import views

urlpatterns = [
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