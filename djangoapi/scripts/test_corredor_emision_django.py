from scripts.p1.django_models.corredor_emision_django import CorredorEmisionDjango


def run():
    corredor = CorredorEmisionDjango()

    d = {
        "codigo_corredor": "COR_DJANGO_001",
        "nombre_corredor": "Corredor Django Avenida Secundaria",
        "municipio": "Bogotá",
        "tipo_via": "Avenida",
        "fuente_emision": "Tráfico vehicular",
        "flujo_vehicular": 18000,
        "velocidad_promedio": 42.5,
        "pm25_estimado": 13.2,
        "no2_estimado": 19.8,
        "categoria_emision": "Media",
        "longitud_km": 1.7,
        "fecha_actualizacion": "2026-05-14",
        "geom": "LINESTRING(1002100 1000200, 1002200 1000300, 1002300 1000500)"
    }

    print("Insertando corredor con Django Model...")
    print(corredor.insert(d))

    print("Consultando todos los corredores con Django Model...")
    print(corredor.selectAllAsDicts())
    