from ui.components.action_card import crear_tarjeta_acciones
from reports import cantidad_indices_por_tabla, detalle_indices, listar_indices


def build(app, pagina):
    crear_tarjeta_acciones(
        pagina,
        "Reportes disponibles",
        [
            ("Listar indices", lambda: app.ejecutar_reporte(listar_indices), True),
            ("Indices por tabla", lambda: app.ejecutar_reporte(cantidad_indices_por_tabla), False),
            ("Detalle de indices", lambda: app.ejecutar_reporte(detalle_indices), False),
        ],
    )
