from scripts.p1.django_models.zona_calidad_aire_django import ZonaCalidadAireDjango


def run():
    zona = ZonaCalidadAireDjango()

    d = {
        "codigo_zona": "ZONA_DJANGO_001",
        "nombre_zona": "Zona Django Centro",
        "municipio": "Bogotá",
        "poblacion": 120000,
        "area_ha": 300.5,
        "pm25_promedio": 11.5,
        "pm10_promedio": 25.3,
        "no2_promedio": 16.4,
        "indice_calidad_aire": 40,
        "categoria_ica": "Buena",
        "fecha_actualizacion": "2026-05-14",
        "geom": "POLYGON((1002000 1000000, 1003000 1000000, 1003000 1001000, 1002000 1001000, 1002000 1000000))"
    }

    print("Insertando zona con Django Model...")
    print(zona.insert(d))

    print("Consultando todas las zonas con Django Model...")
    print(zona.selectAllAsDicts())