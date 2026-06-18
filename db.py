import pyodbc
from config import (
    SERVER,
    DATABASE,
    USERNAME,
    PASSWORD,
    DRIVER,
    USE_WINDOWS_AUTH,
    ENCRYPT,
    TRUST_SERVER_CERTIFICATE
)


def build_connection_string():
    parts = [
        f"DRIVER={{{DRIVER}}}",
        f"SERVER={SERVER}",
        f"DATABASE={DATABASE}",
        f"Encrypt={ENCRYPT}",
        f"TrustServerCertificate={TRUST_SERVER_CERTIFICATE}"
    ]

    if USE_WINDOWS_AUTH:
        parts.append("Trusted_Connection=yes")
    else:
        parts.append(f"UID={USERNAME}")
        parts.append(f"PWD={PASSWORD}")

    return ";".join(parts) + ";"


def get_connection():
    return pyodbc.connect(build_connection_string())


def execute_query(query, params=None):
    conn = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        if params is None:
            cursor.execute(query)
        else:
            cursor.execute(query, *params)

        if cursor.description is None:
            conn.commit()
            return [], []

        columns = [column[0] for column in cursor.description]
        rows = [tuple(row) for row in cursor.fetchall()]

        return columns, rows

    finally:
        if conn is not None:
            conn.close()


def test_connection():
    query = """
    SELECT
        @@SERVERNAME AS servidor,
        DB_NAME() AS base_datos,
        SYSTEM_USER AS usuario_actual;
    """

    return execute_query(query)