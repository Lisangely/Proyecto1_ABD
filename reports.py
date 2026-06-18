import math

from config import (
    SCHEMA,
    PAGE_SIZE_BYTES,
    INDEX_ROW_LOCATOR_BYTES
)

from db import execute_query
from utils import size_of_type, blocking_factor, transfer_time_seconds



def listar_tablas():
    query = """
    SELECT
        t.name AS tabla
    FROM sys.tables t
    INNER JOIN sys.schemas s
        ON t.schema_id = s.schema_id
    WHERE s.name = ?
    ORDER BY t.name;
    """

    return execute_query(query, (SCHEMA,))


def listar_indices():
    query = """
    SELECT
        t.name AS tabla,
        i.name AS indice,
        i.type_desc AS tipo_indice,
        i.is_unique AS es_unico,
        i.is_primary_key AS es_primary_key,
        i.is_disabled AS esta_deshabilitado
    FROM sys.indexes i
    INNER JOIN sys.tables t
        ON i.object_id = t.object_id
    INNER JOIN sys.schemas s
        ON t.schema_id = s.schema_id
    WHERE s.name = ?
      AND i.index_id > 0
      AND i.name IS NOT NULL
      AND i.is_hypothetical = 0
    ORDER BY t.name, i.name;
    """

    return execute_query(query, (SCHEMA,))


def cantidad_indices_por_tabla():
    query = """
    SELECT
        t.name AS tabla,
        COUNT(i.index_id) AS cantidad_indices
    FROM sys.tables t
    INNER JOIN sys.schemas s
        ON t.schema_id = s.schema_id
    LEFT JOIN sys.indexes i
        ON t.object_id = i.object_id
        AND i.index_id > 0
        AND i.name IS NOT NULL
        AND i.is_hypothetical = 0
    WHERE s.name = ?
    GROUP BY t.name
    ORDER BY t.name;
    """

    return execute_query(query, (SCHEMA,))


def cantidad_total_tablas():
    query = """
    SELECT
        COUNT(*) AS cantidad_total_tablas
    FROM sys.tables t
    INNER JOIN sys.schemas s
        ON t.schema_id = s.schema_id
    WHERE s.name = ?;
    """

    return execute_query(query, (SCHEMA,))



def listar_restricciones():
    query = """
    SELECT
        con.name AS restriccion,
        tab.name AS tabla,
        con.type_desc AS tipo_restriccion
    FROM sys.objects con
    INNER JOIN sys.tables tab
        ON con.parent_object_id = tab.object_id
    INNER JOIN sys.schemas s
        ON tab.schema_id = s.schema_id
    WHERE s.name = ?
      AND con.type IN ('PK', 'F', 'UQ', 'C', 'D')
    ORDER BY tab.name, con.type_desc, con.name;
    """

    return execute_query(query, (SCHEMA,))


def detalle_indices():
    query = """
    SELECT
        t.name AS tabla,
        i.name AS indice,
        c.name AS columna,
        ic.key_ordinal AS orden_clave,
        ic.is_included_column AS columna_incluida,
        ic.is_descending_key AS orden_descendente,
        i.is_unique AS es_unico,
        i.type_desc AS tipo_indice,
        i.is_primary_key AS es_primary_key,
        i.is_disabled AS esta_deshabilitado
    FROM sys.indexes i
    INNER JOIN sys.index_columns ic
        ON i.object_id = ic.object_id
       AND i.index_id = ic.index_id
    INNER JOIN sys.columns c
        ON ic.object_id = c.object_id
       AND ic.column_id = c.column_id
    INNER JOIN sys.tables t
        ON i.object_id = t.object_id
    INNER JOIN sys.schemas s
        ON t.schema_id = s.schema_id
    WHERE s.name = ?
      AND i.index_id > 0
      AND i.name IS NOT NULL
      AND i.is_hypothetical = 0
    ORDER BY t.name, i.name, ic.key_ordinal, c.name;
    """

    return execute_query(query, (SCHEMA,))



def listar_triggers():
    query = """
    SELECT
        tr.name AS trigger_name,
        tr.type_desc AS tipo,
        CASE
            WHEN tr.is_disabled = 1 THEN 'Deshabilitado'
            ELSE 'Habilitado'
        END AS estado,
        tb.name AS tabla
    FROM sys.triggers tr
    INNER JOIN sys.tables tb
        ON tr.parent_id = tb.object_id
    INNER JOIN sys.schemas s
        ON tb.schema_id = s.schema_id
    WHERE s.name = ?
    ORDER BY tb.name, tr.name;
    """

    return execute_query(query, (SCHEMA,))



def tamano_tablas():
    query = """
    SELECT
        t.name AS tabla,
        COALESCE(MAX(
            CASE
                WHEN ps.index_id IN (0, 1) THEN ps.row_count
                ELSE 0
            END
        ), 0) AS filas,
        COALESCE(SUM(ps.reserved_page_count), 0) * 8 AS reservado_KB,
        COALESCE(SUM(ps.used_page_count), 0) * 8 AS usado_KB,
        COALESCE(SUM(
            CASE
                WHEN ps.index_id IN (0, 1)
                THEN ps.in_row_data_page_count
                   + ps.lob_used_page_count
                   + ps.row_overflow_used_page_count
                ELSE 0
            END
        ), 0) * 8 AS datos_KB
    FROM sys.tables t
    INNER JOIN sys.schemas s
        ON t.schema_id = s.schema_id
    LEFT JOIN sys.dm_db_partition_stats ps
        ON t.object_id = ps.object_id
    WHERE s.name = ?
    GROUP BY t.name
    ORDER BY usado_KB DESC, t.name;
    """

    return execute_query(query, (SCHEMA,))


def tamano_columnas():
    query = """
    SELECT
        t.name AS tabla,
        c.name AS columna,
        ty.name AS tipo,
        c.max_length,
        c.precision,
        c.scale,
        c.is_nullable
    FROM sys.columns c
    INNER JOIN sys.tables t
        ON c.object_id = t.object_id
    INNER JOIN sys.types ty
        ON c.user_type_id = ty.user_type_id
    INNER JOIN sys.schemas s
        ON t.schema_id = s.schema_id
    WHERE s.name = ?
    ORDER BY t.name, c.column_id;
    """

    _, filas = execute_query(query, (SCHEMA,))

    columnas_resultado = [
        "tabla",
        "columna",
        "tipo",
        "max_length_catalogo",
        "precision",
        "scale",
        "permite_null",
        "tamano_bytes_estimado"
    ]

    filas_resultado = []

    for tabla, columna, tipo, max_length, precision, scale, is_nullable in filas:
        tamano = size_of_type(tipo, max_length, precision, scale)
        permite_null = "SI" if is_nullable else "NO"

        filas_resultado.append(
            (
                tabla,
                columna,
                tipo,
                max_length,
                precision,
                scale,
                permite_null,
                tamano
            )
        )

    return columnas_resultado, filas_resultado


def _columnas_de_tabla(tabla):
    query = """
    SELECT
        c.name AS columna,
        ty.name AS tipo,
        c.max_length,
        c.precision,
        c.scale
    FROM sys.columns c
    INNER JOIN sys.tables t
        ON c.object_id = t.object_id
    INNER JOIN sys.types ty
        ON c.user_type_id = ty.user_type_id
    INNER JOIN sys.schemas s
        ON t.schema_id = s.schema_id
    WHERE s.name = ?
      AND t.name = ?
    ORDER BY c.column_id;
    """

    _, filas = execute_query(query, (SCHEMA, tabla))

    return filas


# ==========================================================
# REQUERIMIENTO 7
# Tamano estimado de cada registro en bytes
# ==========================================================

def calcular_tamano_registro(tabla):
    filas = _columnas_de_tabla(tabla)

    total = 0

    for columna, tipo, max_length, precision, scale in filas:
        total += size_of_type(tipo, max_length, precision, scale)

    return total


def tamano_registros_todas_tablas():
    _, tablas = listar_tablas()

    columnas = [
        "tabla",
        "tamano_registro_bytes"
    ]

    filas = []

    for fila in tablas:
        tabla = fila[0]
        tamano = calcular_tamano_registro(tabla)
        filas.append((tabla, tamano))

    return columnas, filas



def factor_bloqueo(tabla):
    tamano_registro = calcular_tamano_registro(tabla)

    return blocking_factor(tamano_registro)


def factor_bloqueo_todas_tablas():
    _, tablas = listar_tablas()

    columnas = [
        "tabla",
        "tamano_registro_bytes",
        "factor_bloqueo_registros_por_pagina"
    ]

    filas = []

    for fila in tablas:
        tabla = fila[0]
        tamano = calcular_tamano_registro(tabla)
        fb = blocking_factor(tamano)
        filas.append((tabla, tamano, fb))

    return columnas, filas


def _columnas_clave_indices():
    query = """
    SELECT
        t.name AS tabla,
        i.name AS indice,
        c.name AS columna,
        ty.name AS tipo,
        c.max_length,
        c.precision,
        c.scale,
        ic.key_ordinal
    FROM sys.indexes i
    INNER JOIN sys.index_columns ic
        ON i.object_id = ic.object_id
       AND i.index_id = ic.index_id
    INNER JOIN sys.columns c
        ON ic.object_id = c.object_id
       AND ic.column_id = c.column_id
    INNER JOIN sys.types ty
        ON c.user_type_id = ty.user_type_id
    INNER JOIN sys.tables t
        ON i.object_id = t.object_id
    INNER JOIN sys.schemas s
        ON t.schema_id = s.schema_id
    WHERE s.name = ?
      AND i.index_id > 0
      AND i.name IS NOT NULL
      AND i.is_hypothetical = 0
      AND ic.is_included_column = 0
    ORDER BY t.name, i.name, ic.key_ordinal;
    """

    _, filas = execute_query(query, (SCHEMA,))

    return filas


def factor_bloqueo_indices():
    filas_indices = _columnas_clave_indices()

    datos = {}

    for tabla, indice, columna, tipo, max_length, precision, scale, key_ordinal in filas_indices:
        clave = (tabla, indice)

        if clave not in datos:
            datos[clave] = {
                "columnas": [],
                "tamano": INDEX_ROW_LOCATOR_BYTES
            }

        datos[clave]["columnas"].append(columna)
        datos[clave]["tamano"] += size_of_type(tipo, max_length, precision, scale)

    columnas = [
        "tabla",
        "indice",
        "columnas_clave",
        "tamano_registro_indice_bytes",
        "factor_bloqueo_indice"
    ]

    filas = []

    for (tabla, indice), info in datos.items():
        columnas_clave = ", ".join(info["columnas"])
        tamano = info["tamano"]
        fb = blocking_factor(tamano)

        filas.append(
            (
                tabla,
                indice,
                columnas_clave,
                tamano,
                fb
            )
        )

    filas.sort(key=lambda x: (x[0], x[1]))

    return columnas, filas


def tamano_registro_indice(tabla, indice):
    query = """
    SELECT
        c.name AS columna,
        ty.name AS tipo,
        c.max_length,
        c.precision,
        c.scale
    FROM sys.indexes i
    INNER JOIN sys.index_columns ic
        ON i.object_id = ic.object_id
       AND i.index_id = ic.index_id
    INNER JOIN sys.columns c
        ON ic.object_id = c.object_id
       AND ic.column_id = c.column_id
    INNER JOIN sys.types ty
        ON c.user_type_id = ty.user_type_id
    INNER JOIN sys.tables t
        ON i.object_id = t.object_id
    INNER JOIN sys.schemas s
        ON t.schema_id = s.schema_id
    WHERE s.name = ?
      AND t.name = ?
      AND i.name = ?
      AND ic.is_included_column = 0
    ORDER BY ic.key_ordinal;
    """

    _, filas = execute_query(query, (SCHEMA, tabla, indice))

    if not filas:
        return 0

    total = INDEX_ROW_LOCATOR_BYTES

    for columna, tipo, max_length, precision, scale in filas:
        total += size_of_type(tipo, max_length, precision, scale)

    return total


def cantidad_registros(tabla):
    query = """
    SELECT
        COALESCE(SUM(ps.row_count), 0) AS cantidad_registros
    FROM sys.dm_db_partition_stats ps
    INNER JOIN sys.tables t
        ON ps.object_id = t.object_id
    INNER JOIN sys.schemas s
        ON t.schema_id = s.schema_id
    WHERE s.name = ?
      AND t.name = ?
      AND ps.index_id IN (0, 1);
    """

    _, filas = execute_query(query, (SCHEMA, tabla))

    if not filas:
        return 0

    return int(filas[0][0] or 0)


def indices_para_columna(tabla, columna):
    query = """
    SELECT
        t.name AS tabla,
        c.name AS columna,
        i.name AS indice,
        i.type_desc AS tipo_indice,
        i.is_unique AS es_unico,
        ic.key_ordinal AS orden_clave,
        ic.is_included_column AS columna_incluida,
        i.is_disabled AS esta_deshabilitado
    FROM sys.indexes i
    INNER JOIN sys.index_columns ic
        ON i.object_id = ic.object_id
       AND i.index_id = ic.index_id
    INNER JOIN sys.columns c
        ON ic.object_id = c.object_id
       AND ic.column_id = c.column_id
    INNER JOIN sys.tables t
        ON i.object_id = t.object_id
    INNER JOIN sys.schemas s
        ON t.schema_id = s.schema_id
    WHERE s.name = ?
      AND t.name = ?
      AND c.name = ?
      AND i.index_id > 0
      AND i.name IS NOT NULL
      AND i.is_hypothetical = 0
    ORDER BY i.name, ic.key_ordinal;
    """

    return execute_query(query, (SCHEMA, tabla, columna))


def existe_indice(tabla, columna):
    _, filas = indices_para_columna(tabla, columna)

    return len(filas) > 0


def _indice_utilizable_para_igualdad(tabla, columna):
    """
    Para estimar una busqueda de igualdad se considera utilizable
    un indice donde la columna consultada sea la primera columna clave.
    """

    query = """
    SELECT TOP 1
        i.name AS indice,
        i.is_unique AS es_unico,
        i.type_desc AS tipo_indice
    FROM sys.indexes i
    INNER JOIN sys.index_columns ic
        ON i.object_id = ic.object_id
       AND i.index_id = ic.index_id
    INNER JOIN sys.columns c
        ON ic.object_id = c.object_id
       AND ic.column_id = c.column_id
    INNER JOIN sys.tables t
        ON i.object_id = t.object_id
    INNER JOIN sys.schemas s
        ON t.schema_id = s.schema_id
    WHERE s.name = ?
      AND t.name = ?
      AND c.name = ?
      AND i.index_id > 0
      AND i.name IS NOT NULL
      AND i.is_disabled = 0
      AND i.is_hypothetical = 0
      AND ic.is_included_column = 0
      AND ic.key_ordinal = 1
    ORDER BY i.is_unique DESC, i.is_primary_key DESC, i.index_id;
    """

    _, filas = execute_query(query, (SCHEMA, tabla, columna))

    if not filas:
        return None

    return filas[0]


def analizar_costo_igualdad(tabla, columna):
    registros = cantidad_registros(tabla)

    tamano_registro_tabla = calcular_tamano_registro(tabla)
    fb_tabla = blocking_factor(tamano_registro_tabla)

    if fb_tabla > 0:
        bloques_tabla = math.ceil(registros / fb_tabla)
    else:
        bloques_tabla = 0

    indice_info = _indice_utilizable_para_igualdad(tabla, columna)

    if indice_info is not None and registros > 0:
        indice_usado = indice_info[0]
        usa_indice = "SI"

        tamano_indice = tamano_registro_indice(tabla, indice_usado)
        fb_indice = blocking_factor(tamano_indice)

        if fb_indice > 0:
            bloques_indice = math.ceil(registros / fb_indice)
        else:
            bloques_indice = 0

        if bloques_indice <= 1:
            niveles_indice = 1
        elif fb_indice <= 1:
            niveles_indice = bloques_indice
        else:
            niveles_indice = math.ceil(math.log(bloques_indice, fb_indice)) + 1

        accesos_estimados = niveles_indice + 1

        metodo = "Busqueda usando indice. Se estima recorrido del indice mas acceso a pagina de datos."

    else:
        indice_usado = "No aplica"
        usa_indice = "NO"
        tamano_indice = 0
        fb_indice = 0
        accesos_estimados = bloques_tabla

        metodo = "Escaneo completo de la tabla porque no hay indice utilizable como primera columna clave."

    bytes_leidos = accesos_estimados * PAGE_SIZE_BYTES
    tiempo_segundos = transfer_time_seconds(bytes_leidos)

    columnas = [
        "tabla",
        "columna",
        "registros_tabla",
        "tamano_registro_tabla_bytes",
        "factor_bloqueo_tabla",
        "bloques_tabla",
        "indice_utilizado",
        "usa_indice",
        "tamano_registro_indice_bytes",
        "factor_bloqueo_indice",
        "accesos_estimados",
        "bytes_leidos",
        "tiempo_segundos",
        "metodo_estimacion"
    ]

    filas = [
        (
            tabla,
            columna,
            registros,
            tamano_registro_tabla,
            fb_tabla,
            bloques_tabla,
            indice_usado,
            usa_indice,
            tamano_indice,
            fb_indice,
            accesos_estimados,
            bytes_leidos,
            round(tiempo_segundos, 8),
            metodo
        )
    ]

    return columnas, filas


def costo_consulta(tabla, columna):
    _, filas = analizar_costo_igualdad(tabla, columna)

    if not filas:
        return 0, 0

    accesos = filas[0][10]
    tiempo = filas[0][12]

    return accesos, tiempo