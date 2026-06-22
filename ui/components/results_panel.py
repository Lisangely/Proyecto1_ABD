import tkinter as tk
from tkinter import ttk

from ui.components.icon_button import IconButton
from ui.icons import MDL2
from ui.theme import COLORS


class ResultsPanel:
    def __init__(self, padre, on_clear):
        self.status_callback = None
        self._on_clear = on_clear
        self._on_double_click = None
        self._columnas_actuales = []

        card = ttk.Frame(padre, style="Card.TFrame", padding=16)
        card.pack(fill=tk.BOTH, expand=True, pady=(20, 0))

        header = ttk.Frame(card, style="Card.TFrame")
        header.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(header, text="Resultados", style="CardTitle.TLabel").pack(side=tk.LEFT)

        limpiar_frame = tk.Frame(header, bg=COLORS["card"])
        limpiar_frame.pack(side=tk.RIGHT)
        IconButton(
            limpiar_frame,
            MDL2["limpiar"],
            "Limpiar",
            self.limpiar,
            variant="secondary",
        ).pack()

        tree_frame = ttk.Frame(card, style="Card.TFrame")
        tree_frame.pack(fill=tk.BOTH, expand=True)

        self.tree = ttk.Treeview(tree_frame, show="headings")
        self.tree.pack(fill=tk.BOTH, expand=True)
        self.tree.bind("<Double-1>", self._manejar_doble_clic)

        self.lbl_vacio = ttk.Label(
            card,
            text="Selecciona un reporte para ver los resultados aqui.",
            style="CardMuted.TLabel",
        )
        self.lbl_vacio.place(relx=0.5, rely=0.5, anchor="center")

    def set_status_callback(self, callback):
        self.status_callback = callback

    def _formatear_valor(self, valor):
        if valor is None:
            return ""
        if isinstance(valor, float):
            return f"{valor:.8f}"
        return str(valor)

    def _limpiar_tabla(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

    def _mostrar_vacio(self, visible):
        if visible:
            self.lbl_vacio.place(relx=0.5, rely=0.5, anchor="center")
        else:
            self.lbl_vacio.place_forget()

    def limpiar(self, notificar=True):
        self._limpiar_tabla()
        self.tree["columns"] = ()
        self._on_double_click = None
        self._columnas_actuales = []
        self._mostrar_vacio(True)
        if notificar and self._on_clear:
            self._on_clear()

    def _manejar_doble_clic(self, _event):
        if not self._on_double_click:
            return

        seleccion = self.tree.selection()
        if not seleccion:
            return

        valores = self.tree.item(seleccion[0], "values")
        self._on_double_click(self._columnas_actuales, valores)

    def mostrar_datos(self, columnas, filas, on_double_click=None, mensaje_extra=""):
        self._on_double_click = on_double_click
        self._columnas_actuales = list(columnas)
        self._limpiar_tabla()
        self._mostrar_vacio(not filas)

        if not filas:
            if self.status_callback:
                self.status_callback("La consulta no devolvio resultados.")
            return

        self.tree["columns"] = columnas
        self.tree["show"] = "headings"

        for columna in columnas:
            self.tree.heading(columna, text=columna)
            self.tree.column(columna, width=160, minwidth=90, anchor="w", stretch=True)

        for fila in filas:
            valores = [self._formatear_valor(valor) for valor in fila]
            self.tree.insert("", tk.END, values=valores)

        if self.status_callback:
            base = f"Reporte generado. {len(filas)} fila(s)."
            if mensaje_extra:
                base = f"{base} {mensaje_extra}"
            self.status_callback(base)
