from ui.pages import analisis, almacenamiento, indices, inicio, integridad

PAGE_BUILDERS = {
    "inicio": inicio.build,
    "indices": indices.build,
    "integridad": integridad.build,
    "almacenamiento": almacenamiento.build,
    "analisis": analisis.build,
}


def construir_paginas(app):
    paginas = {}

    for seccion_id, builder in PAGE_BUILDERS.items():
        contenedor = app.crear_contenedor_pagina(seccion_id)
        builder(app, contenedor)
        paginas[seccion_id] = contenedor

    return paginas
