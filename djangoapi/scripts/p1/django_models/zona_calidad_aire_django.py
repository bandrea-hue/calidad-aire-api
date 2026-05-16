from django.forms.models import model_to_dict
from django.contrib.gis.geos import GEOSGeometry
from django.db import connection


from calidad_aire.models import ZonaCalidadAire as ZonaCalidadAireModel


EPSG_CODE = 9377
SNAP_DISTANCE = 0.0001


class ZonaCalidadAireDjango:

    contaminantes = [
        "pm25_promedio",
        "pm10_promedio",
        "no2_promedio"
    ]

    required_fields = [
        "codigo_zona",
        "nombre_zona",
        "municipio",
        "geom"
    ]

    def _format_model_dict(self, obj):
        d = model_to_dict(obj)

        d["id"] = obj.id

        if obj.geom:
            d["geom"] = obj.geom.wkt

        if obj.fecha_actualizacion:
            d["fecha_actualizacion"] = obj.fecha_actualizacion.strftime("%Y-%m-%d")

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

    def _validate_polygon_not_intersects_other_polygon(self, geom_wkt, id_to_exclude=None):
        with connection.cursor() as cur:
            if id_to_exclude is None:
                query = """
                SELECT id
                FROM calidad_aire.zona_calidad_aire
                WHERE ST_Relate(
                    geom,
                    ST_SnapToGrid(ST_GeomFromText(%s, %s), %s),
                    'T********'
                )
                """

                cur.execute(query, [geom_wkt, EPSG_CODE, SNAP_DISTANCE])

            else:
                query = """
                SELECT id
                FROM calidad_aire.zona_calidad_aire
                WHERE ST_Relate(
                    geom,
                    ST_SnapToGrid(ST_GeomFromText(%s, %s), %s),
                    'T********'
                )
                AND id <> %s
                """

                cur.execute(query, [geom_wkt, EPSG_CODE, SNAP_DISTANCE, id_to_exclude])

            result = cur.fetchall()

        if len(result) > 0:
            return {
                "ok": False,
                "message": "Polygon interior intersects another polygon",
                "data": result
            }

        return {
            "ok": True,
            "message": "Polygon does not intersect another polygon",
            "data": []
        }

    def _run_common_validations(self, d, id_to_exclude=None):
        required = self._validate_required_fields(d)
        if not required["ok"]:
            return required

        contaminants = self._validate_non_negative_contaminants(d)
        if not contaminants["ok"]:
            return contaminants

        geometry = self._validate_geometry(d["geom"])
        if not geometry["ok"]:
            return geometry

        topology = self._validate_polygon_not_intersects_other_polygon(
            d["geom"],
            id_to_exclude
        )
        if not topology["ok"]:
            return topology

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

            obj = ZonaCalidadAireModel(
                codigo_zona=d.get("codigo_zona"),
                nombre_zona=d.get("nombre_zona"),
                municipio=d.get("municipio"),
                poblacion=d.get("poblacion"),
                area_ha=d.get("area_ha"),
                pm25_promedio=d.get("pm25_promedio"),
                pm10_promedio=d.get("pm10_promedio"),
                no2_promedio=d.get("no2_promedio"),
                indice_calidad_aire=d.get("indice_calidad_aire"),
                categoria_ica=d.get("categoria_ica"),
                fecha_actualizacion=d.get("fecha_actualizacion"),
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
        records = list(ZonaCalidadAireModel.objects.filter(id=d["id"]))

        if len(records) == 0:
            return {
                "ok": False,
                "message": f"The zona_calidad_aire id {d['id']} does not exist",
                "data": []
            }

        obj = records[0]

        return {
            "ok": True,
            "message": "Data retrieved with Django Model",
            "data": [self._format_model_dict(obj)]
        }

    def selectAsTuples(self, d):
        records = list(ZonaCalidadAireModel.objects.filter(id=d["id"]))

        if len(records) == 0:
            return {
                "ok": False,
                "message": f"The zona_calidad_aire id {d['id']} does not exist",
                "data": []
            }

        obj = records[0]

        tup = (
            obj.id,
            obj.codigo_zona,
            obj.nombre_zona,
            obj.municipio,
            obj.poblacion,
            obj.area_ha,
            obj.pm25_promedio,
            obj.pm10_promedio,
            obj.no2_promedio,
            obj.indice_calidad_aire,
            obj.categoria_ica,
            obj.fecha_actualizacion.strftime("%Y-%m-%d") if obj.fecha_actualizacion else None,
            obj.geom.wkt if obj.geom else None
        )

        return {
            "ok": True,
            "message": "Data retrieved as tuples with Django Model",
            "data": [tup]
        }

    def selectAllAsDicts(self):
        records = ZonaCalidadAireModel.objects.all().order_by("id")

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

        records = list(ZonaCalidadAireModel.objects.filter(id=d["id"]))

        if len(records) == 0:
            return {
                "ok": False,
                "message": f"The zona_calidad_aire id {d['id']} does not exist",
                "data": []
            }

        validation = self._run_common_validations(d, d["id"])
        if not validation["ok"]:
            return validation

        try:
            obj = records[0]

            snapped_wkt_geometry = self._get_snapped_wkt_geometry(d["geom"])
            geom = GEOSGeometry(snapped_wkt_geometry, srid=EPSG_CODE)

            obj.codigo_zona = d.get("codigo_zona")
            obj.nombre_zona = d.get("nombre_zona")
            obj.municipio = d.get("municipio")
            obj.poblacion = d.get("poblacion")
            obj.area_ha = d.get("area_ha")
            obj.pm25_promedio = d.get("pm25_promedio")
            obj.pm10_promedio = d.get("pm10_promedio")
            obj.no2_promedio = d.get("no2_promedio")
            obj.indice_calidad_aire = d.get("indice_calidad_aire")
            obj.categoria_ica = d.get("categoria_ica")
            obj.fecha_actualizacion = d.get("fecha_actualizacion")
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
        records = list(ZonaCalidadAireModel.objects.filter(id=d["id"]))

        if len(records) == 0:
            return {
                "ok": False,
                "message": f"The zona_calidad_aire id {d['id']} does not exist",
                "data": []
            }

        obj = records[0]
        obj.delete()

        return {
            "ok": True,
            "message": "Data deleted with Django Model",
            "data": [{"rows_deleted": 1}]
        }