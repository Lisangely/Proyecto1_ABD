import re
from pathlib import Path

import pyodbc

from config import DATABASE, SCHEMA
from db import build_connection_string, get_connection

SQL_DIR = Path(__file__).parent / "sql"

CREATE_TABLES_SCRIPT = SQL_DIR / "create_tables_sqlserver.sql"
INSERT_DATA_SCRIPT = SQL_DIR / "insert_tables_sqlserver.sql"


def _split_sql_batches(content):
    batches = re.split(
        r"^\s*GO\s*;?\s*$",
        content,
        flags=re.MULTILINE | re.IGNORECASE,
    )
    return [batch.strip() for batch in batches if batch.strip()]


def _prepare_batch(batch):
    lines = []

    for line in batch.splitlines():
        if re.match(r"^\s*USE\s+\w+", line, re.IGNORECASE):
            continue
        lines.append(line)

    result = "\n".join(lines).strip()
    return result if result else None


def _execute_sql_file(script_path):
    content = script_path.read_text(encoding="utf-8")
    conn = get_connection()

    try:
        cursor = conn.cursor()

        for batch in _split_sql_batches(content):
            prepared = _prepare_batch(batch)

            if prepared:
                cursor.execute(prepared)

        conn.commit()
    finally:
        conn.close()


def database_exists():
    conn = pyodbc.connect(build_connection_string(database="master"))

    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT 1 FROM sys.databases WHERE name = ?",
            DATABASE,
        )
        return cursor.fetchone() is not None
    finally:
        conn.close()


def ensure_database():
    conn = pyodbc.connect(
        build_connection_string(database="master"),
        autocommit=True,
    )

    try:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            IF NOT EXISTS (
                SELECT 1 FROM sys.databases WHERE name = ?
            )
            BEGIN
                CREATE DATABASE [{DATABASE}];
            END
            """,
            DATABASE,
        )
    finally:
        conn.close()


def ensure_schema():
    conn = get_connection()

    try:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            IF NOT EXISTS (
                SELECT 1 FROM sys.schemas WHERE name = ?
            )
            BEGIN
                EXEC('CREATE SCHEMA [{SCHEMA}]');
            END
            """,
            SCHEMA,
        )
        conn.commit()
    finally:
        conn.close()


def tables_exist():
    conn = get_connection()

    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT 1
            FROM INFORMATION_SCHEMA.TABLES
            WHERE TABLE_SCHEMA = ?
              AND TABLE_NAME = 'serie'
            """,
            SCHEMA,
        )
        return cursor.fetchone() is not None
    finally:
        conn.close()


def has_data():
    conn = get_connection()

    try:
        cursor = conn.cursor()
        cursor.execute(f"SELECT COUNT(*) FROM [{SCHEMA}].[serie]")
        return cursor.fetchone()[0] > 0
    finally:
        conn.close()


def ensure_initialized():
    """
    Crea la base de datos, tablas e inserts si aun no existen.
    Retorna una lista con las acciones realizadas.
    """
    actions = []

    if not database_exists():
        ensure_database()
        actions.append(f"Base de datos '{DATABASE}' creada")

    ensure_schema()

    if not tables_exist():
        if not CREATE_TABLES_SCRIPT.is_file():
            raise FileNotFoundError(
                f"No se encontro el script: {CREATE_TABLES_SCRIPT}"
            )

        _execute_sql_file(CREATE_TABLES_SCRIPT)
        actions.append("Tablas e indices creados")

    if not has_data():
        if not INSERT_DATA_SCRIPT.is_file():
            raise FileNotFoundError(
                f"No se encontro el script: {INSERT_DATA_SCRIPT}"
            )

        _execute_sql_file(INSERT_DATA_SCRIPT)
        actions.append("Datos de prueba insertados")

    return actions
