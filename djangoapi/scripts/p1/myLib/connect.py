import psycopg
from psycopg.rows import dict_row
from myLib import p1Settings


def connect(get_rows_as_dicts=True):
    if get_rows_as_dicts:
        conn = psycopg.connect(
            dbname=p1Settings.POSTGRES_DB,
            user=p1Settings.POSTGRES_USER,
            password=p1Settings.POSTGRES_PASSWORD,
            host=p1Settings.POSTGRES_HOST,
            port=p1Settings.POSTGRES_PORT,
            row_factory=dict_row
        )
    else:
        conn = psycopg.connect(
            dbname=p1Settings.POSTGRES_DB,
            user=p1Settings.POSTGRES_USER,
            password=p1Settings.POSTGRES_PASSWORD,
            host=p1Settings.POSTGRES_HOST,
            port=p1Settings.POSTGRES_PORT
        )

    return conn
