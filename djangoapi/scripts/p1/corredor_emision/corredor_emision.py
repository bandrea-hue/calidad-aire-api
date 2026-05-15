from myLib.connect import connect
from myLib.p1Settings import EPSG_CODE, SNAP_DISTANCE


class CorredorEmision:

    contaminantes = [
        "pm25_estimado",
        "no2_estimado"
    ]

    required_fields = [
        "codigo_corredor",
        "nombre_corredor",
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

    def _validate_line_not_intersects_other_line(self, geom_wkt, id_to_exclude=None):
        conn = connect()
        cur = conn.cursor()

        if id_to_exclude is None:
            query = """
            SELECT id
            FROM calidad_aire.corredor_emision
            WHERE ST_Intersects(
                geom,
                ST_SnapToGrid(ST_GeomFromText(%s, %s), %s)
            )
            """

            cur.execute(query, [geom_wkt, EPSG_CODE, SNAP_DISTANCE])

        else:
            query = """
            SELECT id
            FROM calidad_aire.corredor_emision
            WHERE ST_Intersects(
                geom,
                ST_SnapToGrid(ST_GeomFromText(%s, %s), %s)
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
                "message": "LineString intersects another LineString",
                "data": result
            }

        return {
            "ok": True,
            "message": "LineString does not intersect another LineString",
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

        topology = self._validate_line_not_intersects_other_line(
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
        INSERT INTO calidad_aire.corredor_emision
        (
            codigo_corredor,
            nombre_corredor,
            municipio,
            tipo_via,
            fuente_emision,
            flujo_vehicular,
            velocidad_promedio,
            pm25_estimado,
            no2_estimado,
            categoria_emision,
            longitud_km,
            fecha_actualizacion,
            geom
        )
        VALUES
        (
            %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s,
            %s, %s,
            ST_SnapToGrid(ST_GeomFromText(%s, %s), %s)
        )
        RETURNING id
        """

        values = [
            d.get("codigo_corredor"),
            d.get("nombre_corredor"),
            d.get("municipio"),
            d.get("tipo_via"),
            d.get("fuente_emision"),
            d.get("flujo_vehicular"),
            d.get("velocidad_promedio"),
            d.get("pm25_estimado"),
            d.get("no2_estimado"),
            d.get("categoria_emision"),
            d.get("longitud_km"),
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
            codigo_corredor,
            nombre_corredor,
            municipio,
            tipo_via,
            fuente_emision,
            flujo_vehicular,
            velocidad_promedio,
            pm25_estimado,
            no2_estimado,
            categoria_emision,
            longitud_km,
            fecha_actualizacion,
            ST_AsText(geom) AS geom
        FROM calidad_aire.corredor_emision
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

    def selectAsTuples(self, d):
        conn = connect(get_rows_as_dicts=False)
        cur = conn.cursor()

        query = """
        SELECT
            id,
            codigo_corredor,
            nombre_corredor,
            municipio,
            tipo_via,
            fuente_emision,
            flujo_vehicular,
            velocidad_promedio,
            pm25_estimado,
            no2_estimado,
            categoria_emision,
            longitud_km,
            fecha_actualizacion,
            ST_AsText(geom) AS geom
        FROM calidad_aire.corredor_emision
        WHERE id = %s
        """

        cur.execute(query, [d["id"]])
        result = cur.fetchall()

        cur.close()
        conn.close()

        return {
            "ok": True,
            "message": "Data retrieved as tuples",
            "data": result
        }

    def selectAllAsDicts(self):
        conn = connect()
        cur = conn.cursor()

        query = """
        SELECT
            id,
            codigo_corredor,
            nombre_corredor,
            municipio,
            tipo_via,
            fuente_emision,
            flujo_vehicular,
            velocidad_promedio,
            pm25_estimado,
            no2_estimado,
            categoria_emision,
            longitud_km,
            fecha_actualizacion,
            ST_AsText(geom) AS geom
        FROM calidad_aire.corredor_emision
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
        UPDATE calidad_aire.corredor_emision
        SET
        (
            codigo_corredor,
            nombre_corredor,
            municipio,
            tipo_via,
            fuente_emision,
            flujo_vehicular,
            velocidad_promedio,
            pm25_estimado,
            no2_estimado,
            categoria_emision,
            longitud_km,
            fecha_actualizacion,
            geom
        )
        =
        ROW(
            %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s,
            %s, %s,
            ST_SnapToGrid(ST_GeomFromText(%s, %s), %s)
        )
        WHERE id = %s
        """

        values = [
            d.get("codigo_corredor"),
            d.get("nombre_corredor"),
            d.get("municipio"),
            d.get("tipo_via"),
            d.get("fuente_emision"),
            d.get("flujo_vehicular"),
            d.get("velocidad_promedio"),
            d.get("pm25_estimado"),
            d.get("no2_estimado"),
            d.get("categoria_emision"),
            d.get("longitud_km"),
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
        DELETE FROM calidad_aire.corredor_emision
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