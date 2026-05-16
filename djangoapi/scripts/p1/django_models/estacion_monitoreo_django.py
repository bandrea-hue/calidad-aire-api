from django.forms.models import model_to_dict
from django.contrib.gis.geos import GEOSGeometry
from django.db import connection

from calidad_aire.models import EstacionMonitoreo as EstacionMonitoreoModel


EPSG_CODE = 9377
SNAP_DISTANCE = 0.0001


class EstacionMonitoreoDjango:

    contaminantes = [
        "pm25",
        "pm10",
        "no2",
        "o3",
        "co"
    ]

    required_fields = [
        "codigo_estacion",
        "nombre_estacion",
        "municipio",
        "geom"
    ]

    def _format_model_dict(self, obj):
        d = model_to_dict(obj)

        d["id"] = obj.id

        if obj.geom:
            d["geom"] = obj.geom.wkt

        if obj.fecha_medicion:
            d["fecha_medicion"] = obj.fecha_medicion.strftime("%Y-%m-%d")

        return d

    def _validate_required_fields(self, d):
        for field in self.required_fields:
            if field not in d or d[field] in [None, ""]:
                return {
                    "ok": False,
                    "message": f"The field {field} is mandatory",
                    "data": []
                }

        return {
            "ok": True,
            "message": "Required fields ok",
            "data": []
        }

    def _validate_non_negative_contaminants(self, d):
        for field in self.contaminantes:
            if field in d and d[field] not in [None, ""]:
                if float(d[field]) < 0:
                    return {
                        "ok": False,
                        "message": f"The contaminant {field} can not be negative",
                        "data": []
                    }

        return {
            "ok": True,
            "message": "Contaminants ok",
            "data": []
        }

    def _get_snapped_wkt_geometry(self, geom_wkt):
        with connection.cursor() as cur:
            query = """
            SELECT ST_AsText(
                ST_SnapToGrid(
                    ST_GeomFromText(%s, %s),
                    %s
                )
            )
            """

            cur.execute(query, [geom_wkt, EPSG_CODE, SNAP_DISTANCE])
            snapped_wkt_geometry = cur.fetchall()[0][0]

        return snapped_wkt_geometry

    def _validate_geometry(self, geom_wkt):
        try:
            with connection.cursor() as cur:
                query = """
                SELECT ST_IsValid(
                    ST_SnapToGrid(
                        ST_GeomFromText(%s, %s),
                        %s
                    )
                )
                """

                cur.execute(query, [geom_wkt, EPSG_CODE, SNAP_DISTANCE])
                is_valid = cur.fetchall()[0][0]

            if not is_valid:
                return {
                    "ok": False,
                    "message": "Invalid geometry after ST_SnapToGrid",
                    "data": []
                }

            return {
                "ok": True,
                "message": "Geometry valid",
                "data": []
            }

        except Exception as e:
            return {
                "ok": False,
                "message": f"Geometry error: {str(e)}",
                "data": []
            }

    def _validate_point_inside_zone(self, geom_wkt):
        with connection.cursor() as cur:
            query = """
            SELECT z.id
            FROM calidad_aire.zona_calidad_aire z,
            (
                SELECT ST_SnapToGrid(
                    ST_GeomFromText(%s, %s),
                    %s
                ) AS geom
            ) AS p
            WHERE ST_Within(p.geom, z.geom)
            LIMIT 1
            """

            cur.execute(query, [geom_wkt, EPSG_CODE, SNAP_DISTANCE])
            result = cur.fetchall()

        if len(result) == 0:
            return {
                "ok": False,
                "message": "The monitoring station point is outside every zona_calidad_aire polygon",
                "data": []
            }

        return {
            "ok": True,
            "message": "The point is inside a zona_calidad_aire polygon",
            "data": result
        }

    def _run_common_validations(self, d):
        required = self._validate_required_fields(d)
        if not required["ok"]:
            return required

        contaminants = self._validate_non_negative_contaminants(d)
        if not contaminants["ok"]:
            return contaminants

        geometry = self._validate_geometry(d["geom"])
        if not geometry["ok"]:
            return geometry

        inside = self._validate_point_inside_zone(d["geom"])
        if not inside["ok"]:
            return inside

        return {
            "ok": True,
            "message": "All validations ok",
            "data": []
        }

    def insert(self, d):
        validation = self._run_common_validations(d)
        if not validation["ok"]:
            return validation

        try:
            snapped_wkt_geometry = self._get_snapped_wkt_geometry(d["geom"])
            geom = GEOSGeometry(snapped_wkt_geometry, srid=EPSG_CODE)

            obj = EstacionMonitoreoModel(
                codigo_estacion=d.get("codigo_estacion"),
                nombre_estacion=d.get("nombre_estacion"),
                municipio=d.get("municipio"),
                tipo_estacion=d.get("tipo_estacion"),
                responsable=d.get("responsable"),
                pm25=d.get("pm25"),
                pm10=d.get("pm10"),
                no2=d.get("no2"),
                o3=d.get("o3"),
                co=d.get("co"),
                indice_calidad_aire=d.get("indice_calidad_aire"),
                categoria_ica=d.get("categoria_ica"),
                fecha_medicion=d.get("fecha_medicion"),
                estado=d.get("estado", "Activa"),
                geom=geom
            )

            obj.save()

            return {
                "ok": True,
                "message": "Data inserted with Django Model",
                "data": [{"id": obj.id}]
            }

        except Exception as e:
            return {
                "ok": False,
                "message": str(e),
                "data": []
            }

    def selectAsDicts(self, d):
        records = list(EstacionMonitoreoModel.objects.filter(id=d["id"]))

        if len(records) == 0:
            return {
                "ok": False,
                "message": f"The estacion_monitoreo id {d['id']} does not exist",
                "data": []
            }

        obj = records[0]

        return {
            "ok": True,
            "message": "Data retrieved with Django Model",
            "data": [self._format_model_dict(obj)]
        }

    def selectAsTuples(self, d):
        records = list(EstacionMonitoreoModel.objects.filter(id=d["id"]))

        if len(records) == 0:
            return {
                "ok": False,
                "message": f"The estacion_monitoreo id {d['id']} does not exist",
                "data": []
            }

        obj = records[0]

        tup = (
            obj.id,
            obj.codigo_estacion,
            obj.nombre_estacion,
            obj.municipio,
            obj.tipo_estacion,
            obj.responsable,
            obj.pm25,
            obj.pm10,
            obj.no2,
            obj.o3,
            obj.co,
            obj.indice_calidad_aire,
            obj.categoria_ica,
            obj.fecha_medicion.strftime("%Y-%m-%d") if obj.fecha_medicion else None,
            obj.estado,
            obj.geom.wkt if obj.geom else None
        )

        return {
            "ok": True,
            "message": "Data retrieved as tuples with Django Model",
            "data": [tup]
        }

    def selectAllAsDicts(self):
        records = EstacionMonitoreoModel.objects.all().order_by("id")

        data = []
        for obj in records:
            data.append(self._format_model_dict(obj))

        return {
            "ok": True,
            "message": "Data retrieved with Django Model",
            "data": data
        }

    def update(self, d):
        if "id" not in d or d["id"] in [None, ""]:
            return {
                "ok": False,
                "message": "The id is mandatory for update",
                "data": []
            }

        records = list(EstacionMonitoreoModel.objects.filter(id=d["id"]))

        if len(records) == 0:
            return {
                "ok": False,
                "message": f"The estacion_monitoreo id {d['id']} does not exist",
                "data": []
            }

        validation = self._run_common_validations(d)
        if not validation["ok"]:
            return validation

        try:
            obj = records[0]

            snapped_wkt_geometry = self._get_snapped_wkt_geometry(d["geom"])
            geom = GEOSGeometry(snapped_wkt_geometry, srid=EPSG_CODE)

            obj.codigo_estacion = d.get("codigo_estacion")
            obj.nombre_estacion = d.get("nombre_estacion")
            obj.municipio = d.get("municipio")
            obj.tipo_estacion = d.get("tipo_estacion")
            obj.responsable = d.get("responsable")
            obj.pm25 = d.get("pm25")
            obj.pm10 = d.get("pm10")
            obj.no2 = d.get("no2")
            obj.o3 = d.get("o3")
            obj.co = d.get("co")
            obj.indice_calidad_aire = d.get("indice_calidad_aire")
            obj.categoria_ica = d.get("categoria_ica")
            obj.fecha_medicion = d.get("fecha_medicion")
            obj.estado = d.get("estado", "Activa")
            obj.geom = geom

            obj.save()

            return {
                "ok": True,
                "message": "Data updated with Django Model",
                "data": [{"rows_updated": 1}]
            }

        except Exception as e:
            return {
                "ok": False,
                "message": str(e),
                "data": []
            }

    def delete(self, d):
        records = list(EstacionMonitoreoModel.objects.filter(id=d["id"]))

        if len(records) == 0:
            return {
                "ok": False,
                "message": f"The estacion_monitoreo id {d['id']} does not exist",
                "data": []
            }

        obj = records[0]
        obj.delete()

        return {
            "ok": True,
            "message": "Data deleted with Django Model",
            "data": [{"rows_deleted": 1}]
        }