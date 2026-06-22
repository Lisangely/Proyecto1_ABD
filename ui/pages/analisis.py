import tkinter as tk
from tkinter import ttk

from ui.components.action_card import crear_tarjeta_acciones
from ui.components.icon_button import IconButton
from ui.components.modern_combobox import ModernCombobox
from ui.icons import MDL2
from ui.theme import COLORS
from reports import factor_bloqueo_indices, factor_bloqueo_todas_tablas


def build(app, pagina):
    crear_tarjeta_acciones(
        pagina,
        "Reportes generales",
        [
            ("Factor bloqueo (tablas)", lambda: app.ejecutar_reporte(factor_bloqueo_todas_tablas), True, MDL2["bloqueo"]),
            ("Factor bloqueo (indices)", lambda: app.ejecutar_reporte(factor_bloqueo_indices), False, MDL2["indices"]),
        ],
    )

    form = ttk.Frame(pagina, style="Card.TFrame", padding=16)
    form.pack(fill="x")

    ttk.Label(form, text="Consultas por tabla", style="CardTitle.TLabel").pack(anchor="w", pady=(0, 12))

    campos = ttk.Frame(form, style="Card.TFrame")
    campos.pack(fill="x", pady=(0, 12))

    ttk.Label(campos, text="Tabla", style="Card.TLabel").grid(row=0, column=0, sticky="w", padx=(0, 8), pady=6)
    app.combo_tabla = ModernCombobox(
        campos,
        app.tabla_var,
        width=30,
        on_change=app.cargar_columnas,
    )
    app.combo_tabla.grid(row=0, column=1, sticky="w", padx=(0, 24), pady=6)

    ttk.Label(campos, text="Columna", style="Card.TLabel").grid(row=0, column=2, sticky="w", padx=(0, 8), pady=6)
    app.combo_columna = ModernCombobox(campos, app.columna_var, width=30)
    app.combo_columna.grid(row=0, column=3, sticky="w", pady=6)

    refrescar_frame = tk.Frame(campos, bg=COLORS["card"])
    refrescar_frame.grid(row=0, column=4, padx=(16, 0), pady=6)
    IconButton(
        refrescar_frame,
        MDL2["refrescar"],
        "Refrescar",
        app.refrescar_selectores,
        variant="secondary",
    ).pack()

    botones = tk.Frame(form, bg=COLORS["card"])
    botones.pack(anchor="w")

    IconButton(
        botones,
        MDL2["tamano_registro"],
        "Tamano de registro",
        app.ejecutar_tamano_registro,
        variant="primary",
    ).pack(side="left", padx=(0, 8))

    IconButton(
        botones,
        MDL2["bloqueo"],
        "Factor de bloqueo",
        app.ejecutar_factor_bloqueo_tabla,
        variant="secondary",
    ).pack(side="left", padx=(0, 8))

    IconButton(
        botones,
        MDL2["costo"],
        "Costo de igualdad",
        app.ejecutar_costo_igualdad,
        variant="secondary",
    ).pack(side="left")
