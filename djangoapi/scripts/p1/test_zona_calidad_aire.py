from zona_calidad_aire.zona_calidad_aire import ZonaCalidadAire


def main():
    zona = ZonaCalidadAire()

    d = {
        "codigo_zona": "ZONA001",
        "nombre_zona": "Zona Centro",
        "municipio": "Bogotá",
        "poblacion": 100000,
        "area_ha": 250.5,
        "pm25_promedio": 12.5,
        "pm10_promedio": 28.3,
        "no2_promedio": 18.4,
        "indice_calidad_aire": 45,
        "categoria_ica": "Buena",
        "fecha_actualizacion": "2026-05-14",
        "geom": "POLYGON((1000000 1000000, 1001000 1000000, 1001000 1001000, 1000000 1001000, 1000000 1000000))"
    }

    print(zona.insert(d))
    print(zona.selectAllAsDicts())


if __name__ == "__main__":
    main()