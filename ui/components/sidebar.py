import tkinter as tk

from config import DATABASE, SCHEMA
from ui.components.icon_button import IconButton
from ui.constants import NAV_ITEMS
from ui.icons import MDL2
from ui.theme import COLORS, FONT_FAMILY


class Sidebar:
    def __init__(self, padre, on_navigate):
        self.buttons = {}

        sidebar = tk.Frame(padre, bg=COLORS["sidebar"], width=240)
        sidebar.pack(side=tk.LEFT, fill=tk.Y)
        sidebar.pack_propagate(False)

        header = tk.Frame(sidebar, bg=COLORS["sidebar"], padx=20, pady=24)
        header.pack(fill=tk.X)

        tk.Label(
            header,
            text="StreamUCV",
            font=(FONT_FAMILY, 18, "bold"),
            bg=COLORS["sidebar"],
            fg="#FFFFFF",
        ).pack(anchor="w")

        tk.Label(
            header,
            text="Diccionario de Datos",
            font=(FONT_FAMILY, 10),
            bg=COLORS["sidebar"],
            fg="#94A3B8",
        ).pack(anchor="w", pady=(4, 0))

        nav_frame = tk.Frame(sidebar, bg=COLORS["sidebar"], padx=12, pady=8)
        nav_frame.pack(fill=tk.BOTH, expand=True)

        for seccion_id, etiqueta, icono_key in NAV_ITEMS:
            btn = IconButton(
                nav_frame,
                MDL2[icono_key],
                etiqueta,
                lambda s=seccion_id: on_navigate(s),
                variant="nav",
            )
            btn.pack(fill=tk.X, pady=2)
            self.buttons[seccion_id] = btn

        footer = tk.Frame(sidebar, bg=COLORS["sidebar"], padx=20, pady=20)
        footer.pack(fill=tk.X, side=tk.BOTTOM)

        tk.Label(
            footer,
            text=f"BD: {DATABASE}",
            font=(FONT_FAMILY, 9),
            bg=COLORS["sidebar"],
            fg="#64748B",
        ).pack(anchor="w")

        tk.Label(
            footer,
            text=f"Esquema: {SCHEMA}",
            font=(FONT_FAMILY, 9),
            bg=COLORS["sidebar"],
            fg="#64748B",
        ).pack(anchor="w", pady=(2, 0))

    def set_active(self, seccion_id):
        for sid, btn in self.buttons.items():
            btn.set_variant("nav_active" if sid == seccion_id else "nav")
