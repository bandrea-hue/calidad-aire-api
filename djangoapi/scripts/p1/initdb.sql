CREATE EXTENSION IF NOT EXISTS postgis;

CREATE SCHEMA IF NOT EXISTS calidad_aire;

CREATE TABLE IF NOT EXISTS calidad_aire.zona_calidad_aire (
    id SERIAL PRIMARY KEY,
    codigo_zona VARCHAR(50) UNIQUE NOT NULL,
    nombre_zona VARCHAR(150) NOT NULL,
    municipio VARCHAR(100) NOT NULL,
    poblacion INTEGER,
    area_ha DOUBLE PRECISION,
    pm25_promedio DOUBLE PRECISION,
    pm10_promedio DOUBLE PRECISION,
    no2_promedio DOUBLE PRECISION,
    indice_calidad_aire INTEGER,
    categoria_ica VARCHAR(50),
    fecha_actualizacion DATE,
    geom GEOMETRY(POLYGON, 9377) NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_zona_calidad_aire_geom
ON calidad_aire.zona_calidad_aire
USING GIST (geom);

CREATE TABLE IF NOT EXISTS calidad_aire.corredor_emision (
    id SERIAL PRIMARY KEY,
    codigo_corredor VARCHAR(50) UNIQUE NOT NULL,
    nombre_corredor VARCHAR(150) NOT NULL,
    municipio VARCHAR(100) NOT NULL,
    tipo_via VARCHAR(80),
    fuente_emision VARCHAR(100),
    flujo_vehicular INTEGER,
    velocidad_promedio DOUBLE PRECISION,
    pm25_estimado DOUBLE PRECISION,
    no2_estimado DOUBLE PRECISION,
    categoria_emision VARCHAR(50),
    longitud_km DOUBLE PRECISION,
    fecha_actualizacion DATE,
    geom GEOMETRY(LINESTRING, 9377) NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_corredor_emision_geom
ON calidad_aire.corredor_emision
USING GIST (geom);

CREATE TABLE IF NOT EXISTS calidad_aire.estacion_monitoreo (
    id SERIAL PRIMARY KEY,
    codigo_estacion VARCHAR(50) UNIQUE NOT NULL,
    nombre_estacion VARCHAR(150) NOT NULL,
    municipio VARCHAR(100) NOT NULL,
    tipo_estacion VARCHAR(80),
    responsable VARCHAR(120),
    pm25 DOUBLE PRECISION,
    pm10 DOUBLE PRECISION,
    no2 DOUBLE PRECISION,
    o3 DOUBLE PRECISION,
    co DOUBLE PRECISION,
    indice_calidad_aire INTEGER,
    categoria_ica VARCHAR(50),
    fecha_medicion DATE,
    estado VARCHAR(30) DEFAULT 'Activa',
    geom GEOMETRY(POINT, 9377) NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_estacion_monitoreo_geom
ON calidad_aire.estacion_monitoreo
USING GIST (geom);