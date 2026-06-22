from ui.components.action_card import crear_tarjeta_acciones
from reports import listar_restricciones, listar_triggers


def build(app, pagina):
    crear_tarjeta_acciones(
        pagina,
        "Reportes disponibles",
        [
            ("Listar restricciones", lambda: app.ejecutar_reporte(
                listar_restricciones,
                on_double_click=app.mostrar_sql_restriccion,
                mensaje_extra="Doble clic en una fila para ver el SQL.",
            ), True),
            ("Listar triggers", lambda: app.ejecutar_reporte(
                listar_triggers,
                on_double_click=app.mostrar_sql_trigger,
                mensaje_extra="Doble clic en una fila para ver el SQL.",
            ), False),
        ],
    )
