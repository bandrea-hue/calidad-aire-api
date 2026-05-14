from myLib.connect import connect


def main():
    conn = connect()
    cur = conn.cursor()

    query = """
    SELECT table_schema, table_name
    FROM information_schema.tables
    WHERE table_schema = 'calidad_aire'
    ORDER BY table_name
    """

    cur.execute(query)
    result = cur.fetchall()

    print(result)

    cur.close()
    conn.close()


if __name__ == "__main__":
    main()