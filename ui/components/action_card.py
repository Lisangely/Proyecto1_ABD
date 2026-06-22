from ui.components.icon_button import IconButton
from ui.icons import MDL2


def crear_tarjeta_acciones(padre, titulo, acciones, empaquetar=True, columnas_botones=3):
    from tkinter import ttk

    card = ttk.Frame(padre, style="Card.TFrame", padding=16)
    if empaquetar:
        card.pack(fill="x", pady=(0, 12))

    ttk.Label(card, text=titulo, style="CardTitle.TLabel").pack(anchor="w", pady=(0, 10))

    botones = ttk.Frame(card, style="Card.TFrame")
    botones.pack(fill="x")

    iconos_por_defecto = {
        "Listar": MDL2["listar"],
        "Total": MDL2["total"],
        "Detalle": MDL2["reporte"],
        "Indices": MDL2["indices"],
        "restricciones": MDL2["restricciones"],
        "triggers": MDL2["triggers"],
        "Tamano": MDL2["tamano_tabla"],
        "Factor": MDL2["bloqueo"],
    }

    for index, accion in enumerate(acciones):
        if len(accion) == 4:
            texto, comando, primario, icono = accion
        else:
            texto, comando, primario = accion
            icono = _resolver_icono(texto, iconos_por_defecto)

        variant = "primary" if primario else "secondary"
        btn = IconButton(botones, icono, texto, comando, variant=variant)
        btn.grid(row=index // columnas_botones, column=index % columnas_botones, padx=(0, 8), pady=(0, 8), sticky="w")

    return card


def _resolver_icono(texto, mapa):
    texto_lower = texto.lower()
    for clave, icono in mapa.items():
        if clave.lower() in texto_lower:
            return icono
    return MDL2["reporte"]
