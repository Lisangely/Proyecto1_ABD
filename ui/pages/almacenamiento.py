from ui.components.action_card import crear_tarjeta_acciones
from reports import tamano_columnas, tamano_registros_todas_tablas, tamano_tablas


def build(app, pagina):
    crear_tarjeta_acciones(
        pagina,
        "Reportes disponibles",
        [
            ("Tamano de tablas", lambda: app.ejecutar_reporte(tamano_tablas), True),
            ("Tamano de registros", lambda: app.ejecutar_reporte(tamano_registros_todas_tablas), False),
            ("Tamano de columnas", lambda: app.ejecutar_reporte(tamano_columnas), False),
        ],
    )
