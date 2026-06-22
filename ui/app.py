import tkinter as tk
from tkinter import messagebox, ttk

from config import SERVER
from db import test_connection
from reports import (
    analizar_costo_igualdad,
    calcular_tamano_registro,
    factor_bloqueo,
    listar_tablas,
    nombres_columnas,
    obtener_sql_restriccion,
    obtener_sql_trigger,
)
from ui.components.detail_dialog import mostrar_detalle
from ui.components.results_panel import ResultsPanel
from ui.components.sidebar import Sidebar
from ui.constants import SECCIONES
from ui.pages import construir_paginas
from ui.theme import COLORS, configurar_estilos


class StreamUCVApp:
    def __init__(self, ventana):
        self.ventana = ventana
        self.status_var = tk.StringVar(value="Listo")
        self.tabla_var = tk.StringVar()
        self.columna_var = tk.StringVar()
        self.combo_tabla = None
        self.combo_columna = None
        self.paginas = {}
        self.frame_contenido = None

        configurar_estilos()
        self._construir_layout()
        self.mostrar_seccion("inicio")
        self.cargar_tablas()

    def _construir_layout(self):
        self.ventana.configure(bg=COLORS["bg"])

        contenedor = ttk.Frame(self.ventana)
        contenedor.pack(fill=tk.BOTH, expand=True)

        self.sidebar = Sidebar(contenedor, on_navigate=self.mostrar_seccion)

        main = ttk.Frame(contenedor, padding=(28, 24, 28, 16))
        main.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.lbl_titulo = ttk.Label(main, text="", style="Title.TLabel")
        self.lbl_titulo.pack(anchor="w")

        self.lbl_descripcion = ttk.Label(main, text="", style="Muted.TLabel", wraplength=900)
        self.lbl_descripcion.pack(anchor="w", pady=(6, 20))

        self.frame_contenido = ttk.Frame(main)
        self.frame_contenido.pack(fill=tk.X)

        self.paginas = construir_paginas(self)

        self.resultados = ResultsPanel(main, on_clear=self._on_limpiar_resultados)
        self.resultados.set_status_callback(self._set_status)

        status_bar = ttk.Frame(main)
        status_bar.pack(fill=tk.X, pady=(12, 0))

        ttk.Label(status_bar, textvariable=self.status_var, style="Muted.TLabel").pack(side=tk.LEFT)
        ttk.Label(status_bar, text=f"Servidor: {SERVER}", style="Muted.TLabel").pack(side=tk.RIGHT)

    def crear_contenedor_pagina(self, seccion_id):
        return ttk.Frame(self.frame_contenido, name=seccion_id)

    def mostrar_seccion(self, seccion_id):
        info = SECCIONES[seccion_id]

        self.lbl_titulo.configure(text=info["titulo"])
        self.lbl_descripcion.configure(text=info["descripcion"])

        for pagina in self.paginas.values():
            pagina.pack_forget()

        self.paginas[seccion_id].pack(fill=tk.X)
        self.sidebar.set_active(seccion_id)
        self.resultados.limpiar(notificar=False)
        self._set_status(f"Seccion: {info['titulo']}")

    def _set_status(self, mensaje):
        self.status_var.set(mensaje)

    def _on_limpiar_resultados(self):
        self._set_status("Resultados limpiados.")

    def ejecutar_reporte(self, funcion, on_double_click=None, mensaje_extra=""):
        try:
            columnas, filas = funcion()
            self.resultados.mostrar_datos(
                columnas,
                filas,
                on_double_click=on_double_click,
                mensaje_extra=mensaje_extra,
            )
        except Exception as error:
            messagebox.showerror("Error", str(error))
            self._set_status("Ocurrio un error al generar el reporte.")

    def mostrar_sql_restriccion(self, columnas, fila):
        try:
            restriccion = fila[columnas.index("restriccion")]
            tabla = fila[columnas.index("tabla")]
            sql = obtener_sql_restriccion(restriccion, tabla)

            if not sql:
                messagebox.showinfo(
                    "Sin definicion",
                    f"No se encontro el SQL para la restriccion '{restriccion}'.",
                )
                return

            titulo = f"{restriccion} ({tabla})"
            mostrar_detalle(titulo, sql, self.ventana)
        except Exception as error:
            messagebox.showerror("Error", str(error))

    def mostrar_sql_trigger(self, columnas, fila):
        try:
            trigger_name = fila[columnas.index("trigger_name")]
            tabla = fila[columnas.index("tabla")]
            sql = obtener_sql_trigger(trigger_name, tabla)

            if not sql:
                messagebox.showinfo(
                    "Sin definicion",
                    f"No se encontro el SQL para el trigger '{trigger_name}'.",
                )
                return

            titulo = f"{trigger_name} ({tabla})"
            mostrar_detalle(titulo, sql, self.ventana)
        except Exception as error:
            messagebox.showerror("Error", str(error))

    def probar_conexion(self):
        try:
            columnas, filas = test_connection()
            self.resultados.mostrar_datos(columnas, filas)
            self._set_status("Conexion exitosa.")
        except Exception as error:
            messagebox.showerror("Error de conexion", str(error))
            self._set_status("No se pudo conectar a la base de datos.")

    def ejecutar_tamano_registro(self):
        try:
            tabla = self.tabla_var.get().strip()
            if not tabla:
                messagebox.showwarning("Dato faltante", "Selecciona una tabla.")
                return

            tamano = calcular_tamano_registro(tabla)
            self.resultados.mostrar_datos(
                ["tabla", "tamano_registro_bytes"],
                [(tabla, tamano)],
            )
        except Exception as error:
            messagebox.showerror("Error", str(error))

    def ejecutar_factor_bloqueo_tabla(self):
        try:
            tabla = self.tabla_var.get().strip()
            if not tabla:
                messagebox.showwarning("Dato faltante", "Selecciona una tabla.")
                return

            fb = factor_bloqueo(tabla)
            tamano = calcular_tamano_registro(tabla)
            self.resultados.mostrar_datos(
                ["tabla", "tamano_registro_bytes", "factor_bloqueo_registros_por_pagina"],
                [(tabla, tamano, fb)],
            )
        except Exception as error:
            messagebox.showerror("Error", str(error))

    def ejecutar_costo_igualdad(self):
        try:
            tabla = self.tabla_var.get().strip()
            columna = self.columna_var.get().strip()

            if not tabla:
                messagebox.showwarning("Dato faltante", "Selecciona una tabla.")
                return
            if not columna:
                messagebox.showwarning("Dato faltante", "Selecciona una columna.")
                return

            columnas, filas = analizar_costo_igualdad(tabla, columna)
            self.resultados.mostrar_datos(columnas, filas)
        except Exception as error:
            messagebox.showerror("Error", str(error))

    def refrescar_selectores(self):
        self.cargar_tablas()
        self.cargar_columnas()

    def cargar_tablas(self):
        try:
            _, filas = listar_tablas()
            nombres = [fila[0] for fila in filas]

            if self.combo_tabla is not None:
                self.combo_tabla.set_values(nombres)

            if nombres and not self.tabla_var.get():
                self.tabla_var.set(nombres[0])

            self.cargar_columnas()
            self._set_status(f"{len(nombres)} tablas disponibles.")
        except Exception:
            self._set_status("No se pudieron cargar las tablas. Revisa la conexion.")

    def cargar_columnas(self):
        tabla = self.tabla_var.get().strip()

        if not tabla:
            if self.combo_columna is not None:
                self.combo_columna.set_values([])
            self.columna_var.set("")
            return

        try:
            columnas = nombres_columnas(tabla)

            if self.combo_columna is not None:
                self.combo_columna.set_values(columnas)

            if columnas:
                if self.columna_var.get() not in columnas:
                    self.columna_var.set(columnas[0])
            else:
                self.columna_var.set("")
        except Exception:
            if self.combo_columna is not None:
                self.combo_columna.set_values([])
            self.columna_var.set("")
