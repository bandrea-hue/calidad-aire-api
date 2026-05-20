from django.contrib import admin

# Register your models here.
from .models import ZonaCalidadAire, CorredorEmision, EstacionMonitoreo

admin.site.register(ZonaCalidadAire)
admin.site.register(CorredorEmision)
admin.site.register(EstacionMonitoreo)