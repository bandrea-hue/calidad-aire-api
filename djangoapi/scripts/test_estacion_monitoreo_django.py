from scripts.p1.django_models.estacion_monitoreo_django import EstacionMonitoreoDjango


def run():
    estacion = EstacionMonitoreoDjango()

    d = {
        "codigo_estacion": "EST_DJANGO_001",
        "nombre_estacion": "Estación Django Centro",
        "municipio": "Bogotá",
        "tipo_estacion": "Urbana",
        "responsable": "Autoridad Ambiental",
        "pm25": 10.5,
        "pm10": 24.2,
        "no2": 16.7,
        "o3": 20.1,
        "co": 0.6,
        "indice_calidad_aire": 38,
        "categoria_ica": "Buena",
        "fecha_medicion": "2026-05-14",
        "estado": "Activa",
        "geom": "POINT(1000500 1000500)"
    }

    print("Insertando estación con Django Model...")
    print(estacion.insert(d))

    print("Consultando todas las estaciones con Django Model...")
    print(estacion.selectAllAsDicts())