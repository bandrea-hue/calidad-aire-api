from corredor_emision.corredor_emision import CorredorEmision


def main():
    corredor = CorredorEmision()

    d = {
        "codigo_corredor": "COR001",
        "nombre_corredor": "Corredor Avenida Principal",
        "municipio": "Bogotá",
        "tipo_via": "Avenida",
        "fuente_emision": "Tráfico vehicular",
        "flujo_vehicular": 25000,
        "velocidad_promedio": 35.5,
        "pm25_estimado": 15.2,
        "no2_estimado": 22.8,
        "categoria_emision": "Media",
        "longitud_km": 1.4,
        "fecha_actualizacion": "2026-05-14",
        "geom": "LINESTRING(1000100 1000100, 1000200 1000200, 1000300 1000250)"
    }

    print(corredor.insert(d))
    print(corredor.selectAllAsDicts())


if __name__ == "__main__":
    main()