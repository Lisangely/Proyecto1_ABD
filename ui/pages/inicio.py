import tkinter as tk
from tkinter import ttk

from config import DATABASE, SCHEMA, SERVER
from ui.components.icon_button import IconButton
from ui.icons import MDL2
from reports import cantidad_total_tablas, listar_tablas


def build(app, pagina):
    info = ttk.Frame(pagina, style="Card.TFrame", padding=20)
    info.pack(fill="x")

    ttk.Label(info, text="Conexion activa", style="CardTitle.TLabel").pack(anchor="w")
    ttk.Label(
        info,
        text=f"Servidor: {SERVER}  |  Base de datos: {DATABASE}  |  Esquema: {SCHEMA}",
        style="CardMuted.TLabel",
    ).pack(anchor="w", pady=(8, 16))

    acciones = tk.Frame(info, bg="#FFFFFF")
    acciones.pack(anchor="w")

    IconButton(
        acciones,
        MDL2["conexion"],
        "Probar conexion",
        app.probar_conexion,
        variant="primary",
    ).pack(side="left", padx=(0, 8))

    IconButton(
        acciones,
        MDL2["total"],
        "Ver total de tablas",
        lambda: app.ejecutar_reporte(cantidad_total_tablas),
        variant="secondary",
    ).pack(side="left", padx=(0, 8))

    IconButton(
        acciones,
        MDL2["tablas"],
        "Listar tablas",
        lambda: app.ejecutar_reporte(listar_tablas),
        variant="secondary",
    ).pack(side="left")
