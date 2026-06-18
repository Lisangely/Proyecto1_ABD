from config import PAGE_SIZE_BYTES, TRANSFER_SPEED_MB_PER_SEC


def to_int(value, default=0):
    try:
        if value is None:
            return default
        return int(value)
    except Exception:
        return default


def size_of_type(tipo, max_length, precision=None, scale=None):
    """
    Devuelve el tamano estimado en bytes de una columna.
    Para char, varchar, nchar, nvarchar y varbinary se usa max_length,
    porque SQL Server lo guarda en bytes en sys.columns.
    """

    if tipo is None:
        return 0

    tipo = str(tipo).lower()
    max_length = to_int(max_length)
    precision = to_int(precision)
    scale = to_int(scale)

    fixed_sizes = {
        "bit": 1,
        "tinyint": 1,
        "smallint": 2,
        "int": 4,
        "bigint": 8,
        "real": 4,
        "float": 8,
        "smallmoney": 4,
        "money": 8,
        "date": 3,
        "smalldatetime": 4,
        "datetime": 8,
        "uniqueidentifier": 16,
        "timestamp": 8,
        "rowversion": 8
    }

    if tipo in fixed_sizes:
        return fixed_sizes[tipo]

    if tipo in ("decimal", "numeric"):
        if precision <= 9:
            return 5
        elif precision <= 19:
            return 9
        elif precision <= 28:
            return 13
        else:
            return 17

    if tipo == "time":
        if scale <= 2:
            return 3
        elif scale <= 4:
            return 4
        else:
            return 5

    if tipo == "datetime2":
        if scale <= 2:
            return 6
        elif scale <= 4:
            return 7
        else:
            return 8

    if tipo == "datetimeoffset":
        if scale <= 2:
            return 8
        elif scale <= 4:
            return 9
        else:
            return 10

    if tipo in ("char", "varchar", "nchar", "nvarchar", "binary", "varbinary"):
        if max_length == -1:
            return 8000
        return max(0, max_length)

    if tipo in ("text", "ntext", "image", "xml"):
        return 16

    if max_length > 0:
        return max_length

    return 0


def blocking_factor(record_size):
    if record_size <= 0:
        return 0

    return max(1, PAGE_SIZE_BYTES // record_size)


def transfer_time_seconds(bytes_amount):
    bytes_per_second = TRANSFER_SPEED_MB_PER_SEC * 1024 * 1024

    if bytes_per_second <= 0:
        return 0

    return bytes_amount / bytes_per_second