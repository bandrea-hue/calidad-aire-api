from estacion_monitoreo.estacion_monitoreo import EstacionMonitoreo


def main():
    estacion = EstacionMonitoreo()

    d = {
        "codigo_estacion": "EST001",
        "nombre_estacion": "Estación Centro",
        "municipio": "Bogotá",
        "tipo_estacion": "Urbana",
        "responsable": "Autoridad Ambiental",
        "pm25": 12.5,
        "pm10": 30.2,
        "no2": 18.7,
        "o3": 22.1,
        "co": 0.8,
        "indice_calidad_aire": 45,
        "categoria_ica": "Buena",
        "fecha_medicion": "2026-05-14",
        "estado": "Activa",
        "geom": "POINT(1000500 1000500)"
    }

    print(estacion.insert(d))
    print(estacion.selectAllAsDicts())


if __name__ == "__main__":
    main()