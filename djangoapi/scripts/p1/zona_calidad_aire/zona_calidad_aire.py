from myLib.connect import connect
from myLib.p1Settings import EPSG_CODE, SNAP_DISTANCE


class ZonaCalidadAire:

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

    def _validate_required_fields(self, d):
        for field in self.required_fields:
            if field not in d or d[field] in [None, ""]:
                return {
                    "ok": False,
                    "message": f"The field {field} is mandatory",
                    "data": []
                }

        return {"ok": True, "message": "Required fields ok", "data": []}

    def _validate_non_negative_contaminants(self, d):
        for field in self.contaminantes:
            if field in d and d[field] not in [None, ""]:
                if float(d[field]) < 0:
                    return {
                        "ok": False,
                        "message": f"The contaminant {field} can not be negative",
                        "data": []
                    }

        return {"ok": True, "message": "Contaminants ok", "data": []}

    def _validate_geometry(self, geom_wkt):
        conn = connect()
        cur = conn.cursor()

        query = """
        SELECT ST_IsValid(
            ST_SnapToGrid(
                ST_GeomFromText(%s, %s),
                %s
            )
        ) AS is_valid
        """

        cur.execute(query, [geom_wkt, EPSG_CODE, SNAP_DISTANCE])
        result = cur.fetchall()

        cur.close()
        conn.close()

        if not result[0]["is_valid"]:
            return {
                "ok": False,
                "message": "Invalid geometry after ST_SnapToGrid",
                "data": []
            }

        return {"ok": True, "message": "Geometry valid", "data": []}

    def _validate_polygon_not_intersects_other_polygon(self, geom_wkt, id_to_exclude=None):
        conn = connect()
        cur = conn.cursor()

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

        cur.close()
        conn.close()

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

        return {"ok": True, "message": "All validations ok", "data": []}

    def insert(self, d):
        validation = self._run_common_validations(d)
        if not validation["ok"]:
            return validation

        conn = connect()
        cur = conn.cursor()

        query = """
        INSERT INTO calidad_aire.zona_calidad_aire
        (
            codigo_zona,
            nombre_zona,
            municipio,
            poblacion,
            area_ha,
            pm25_promedio,
            pm10_promedio,
            no2_promedio,
            indice_calidad_aire,
            categoria_ica,
            fecha_actualizacion,
            geom
        )
        VALUES
        (
            %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s,
            %s,
            ST_SnapToGrid(ST_GeomFromText(%s, %s), %s)
        )
        RETURNING id
        """

        values = [
            d.get("codigo_zona"),
            d.get("nombre_zona"),
            d.get("municipio"),
            d.get("poblacion"),
            d.get("area_ha"),
            d.get("pm25_promedio"),
            d.get("pm10_promedio"),
            d.get("no2_promedio"),
            d.get("indice_calidad_aire"),
            d.get("categoria_ica"),
            d.get("fecha_actualizacion"),
            d.get("geom"),
            EPSG_CODE,
            SNAP_DISTANCE
        ]

        try:
            cur.execute(query, values)
            conn.commit()
            result = cur.fetchall()

            return {
                "ok": True,
                "message": "Data inserted",
                "data": [{"id": result[0]["id"]}]
            }

        except Exception as e:
            conn.rollback()
            return {
                "ok": False,
                "message": str(e),
                "data": []
            }

        finally:
            cur.close()
            conn.close()

    def selectAsDicts(self, d):
        conn = connect()
        cur = conn.cursor()

        query = """
        SELECT
            id,
            codigo_zona,
            nombre_zona,
            municipio,
            poblacion,
            area_ha,
            pm25_promedio,
            pm10_promedio,
            no2_promedio,
            indice_calidad_aire,
            categoria_ica,
            fecha_actualizacion,
            ST_AsText(geom) AS geom
        FROM calidad_aire.zona_calidad_aire
        WHERE id = %s
        """

        cur.execute(query, [d["id"]])
        result = cur.fetchall()

        cur.close()
        conn.close()

        return {
            "ok": True,
            "message": "Data retrieved",
            "data": result
        }

    def selectAllAsDicts(self):
        conn = connect()
        cur = conn.cursor()

        query = """
        SELECT
            id,
            codigo_zona,
            nombre_zona,
            municipio,
            poblacion,
            area_ha,
            pm25_promedio,
            pm10_promedio,
            no2_promedio,
            indice_calidad_aire,
            categoria_ica,
            fecha_actualizacion,
            ST_AsText(geom) AS geom
        FROM calidad_aire.zona_calidad_aire
        ORDER BY id
        """

        cur.execute(query)
        result = cur.fetchall()

        cur.close()
        conn.close()

        return {
            "ok": True,
            "message": "Data retrieved",
            "data": result
        }

    def update(self, d):
        if "id" not in d or d["id"] in [None, ""]:
            return {
                "ok": False,
                "message": "The id is mandatory for update",
                "data": []
            }

        validation = self._run_common_validations(d, d["id"])
        if not validation["ok"]:
            return validation

        conn = connect()
        cur = conn.cursor()

        query = """
        UPDATE calidad_aire.zona_calidad_aire
        SET
        (
            codigo_zona,
            nombre_zona,
            municipio,
            poblacion,
            area_ha,
            pm25_promedio,
            pm10_promedio,
            no2_promedio,
            indice_calidad_aire,
            categoria_ica,
            fecha_actualizacion,
            geom
        )
        =
        ROW(
            %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s,
            %s,
            ST_SnapToGrid(ST_GeomFromText(%s, %s), %s)
        )
        WHERE id = %s
        """

        values = [
            d.get("codigo_zona"),
            d.get("nombre_zona"),
            d.get("municipio"),
            d.get("poblacion"),
            d.get("area_ha"),
            d.get("pm25_promedio"),
            d.get("pm10_promedio"),
            d.get("no2_promedio"),
            d.get("indice_calidad_aire"),
            d.get("categoria_ica"),
            d.get("fecha_actualizacion"),
            d.get("geom"),
            EPSG_CODE,
            SNAP_DISTANCE,
            d.get("id")
        ]

        try:
            cur.execute(query, values)
            conn.commit()

            return {
                "ok": True,
                "message": "Data updated",
                "data": [{"rows_updated": cur.rowcount}]
            }

        except Exception as e:
            conn.rollback()
            return {
                "ok": False,
                "message": str(e),
                "data": []
            }

        finally:
            cur.close()
            conn.close()

    def delete(self, d):
        conn = connect()
        cur = conn.cursor()

        query = """
        DELETE FROM calidad_aire.zona_calidad_aire
        WHERE id = %s
        """

        try:
            cur.execute(query, [d["id"]])
            conn.commit()

            return {
                "ok": True,
                "message": "Data deleted",
                "data": [{"rows_deleted": cur.rowcount}]
            }

        except Exception as e:
            conn.rollback()
            return {
                "ok": False,
                "message": str(e),
                "data": []
            }

        finally:
            cur.close()
            conn.close()