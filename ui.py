import tkinter as tk
from tkinter import ttk, messagebox

from config import SERVER, DATABASE, SCHEMA

from db import test_connection

from reports import (
    listar_tablas,
    listar_indices,
    cantidad_total_tablas,
    cantidad_indices_por_tabla,
    listar_restricciones,
    detalle_indices,
    listar_triggers,
    tamano_tablas,
    tamano_columnas,
    tamano_registros_todas_tablas,
    calcular_tamano_registro,
    factor_bloqueo,
    factor_bloqueo_todas_tablas,
    factor_bloqueo_indices,
    analizar_costo_igualdad
)


def iniciar_app():
    ventana = tk.Tk()
    ventana.title("StreamUCV - Diccionario de Datos")
    ventana.geometry("1250x750")
    ventana.minsize(1000, 650)

    main_frame = ttk.Frame(ventana, padding=10)
    main_frame.pack(fill=tk.BOTH, expand=True)

    titulo = ttk.Label(
        main_frame,
        text="StreamUCV - Reportes del Diccionario de Datos",
        font=("Arial", 16, "bold")
    )
    titulo.pack(anchor="w")

    subtitulo = ttk.Label(
        main_frame,
        text=f"Servidor: {SERVER}, Base de datos: {DATABASE}, Esquema: {SCHEMA}"
    )
    subtitulo.pack(anchor="w", pady=(0, 10))

    status_var = tk.StringVar(value="Listo")



    def formatear_valor(valor):
        if valor is None:
            return ""

        if isinstance(valor, float):
            return f"{valor:.8f}"

        return str(valor)

    def limpiar_tabla():
        for item in tree.get_children():
            tree.delete(item)

    def mostrar_datos(columnas, filas):
        limpiar_tabla()

        tree["columns"] = columnas
        tree["show"] = "headings"

        for columna in columnas:
            tree.heading(columna, text=columna)
            tree.column(columna, width=180, minwidth=100, anchor="w", stretch=True)

        for fila in filas:
            valores = [formatear_valor(valor) for valor in fila]
            tree.insert("", tk.END, values=valores)

        status_var.set(f"Reporte generado correctamente. Filas: {len(filas)}")

    def mostrar_mensaje(titulo_mensaje, mensaje):
        columnas = ["mensaje"]
        filas = [(f"{titulo_mensaje}: {mensaje}",)]
        mostrar_datos(columnas, filas)

    def ejecutar_reporte(funcion):
        try:
            columnas, filas = funcion()
            mostrar_datos(columnas, filas)
        except Exception as error:
            messagebox.showerror("Error", str(error))
            status_var.set("Ocurrio un error al generar el reporte.")

    def obtener_tabla():
        return tabla_var.get().strip()

    def obtener_columna():
        return columna_var.get().strip()

    def ejecutar_tamano_registro():
        try:
            tabla = obtener_tabla()

            if not tabla:
                messagebox.showwarning("Dato faltante", "Debes escribir o seleccionar una tabla.")
                return

            tamano = calcular_tamano_registro(tabla)

            columnas = [
                "tabla",
                "tamano_registro_bytes"
            ]

            filas = [
                (tabla, tamano)
            ]

            mostrar_datos(columnas, filas)

        except Exception as error:
            messagebox.showerror("Error", str(error))

    def ejecutar_factor_bloqueo_tabla():
        try:
            tabla = obtener_tabla()

            if not tabla:
                messagebox.showwarning("Dato faltante", "Debes escribir o seleccionar una tabla.")
                return

            fb = factor_bloqueo(tabla)
            tamano = calcular_tamano_registro(tabla)

            columnas = [
                "tabla",
                "tamano_registro_bytes",
                "factor_bloqueo_registros_por_pagina"
            ]

            filas = [
                (tabla, tamano, fb)
            ]

            mostrar_datos(columnas, filas)

        except Exception as error:
            messagebox.showerror("Error", str(error))

    def ejecutar_costo_igualdad():
        try:
            tabla = obtener_tabla()
            columna = obtener_columna()

            if not tabla:
                messagebox.showwarning("Dato faltante", "Debes escribir o seleccionar una tabla.")
                return

            if not columna:
                messagebox.showwarning("Dato faltante", "Debes escribir una columna.")
                return

            columnas, filas = analizar_costo_igualdad(tabla, columna)
            mostrar_datos(columnas, filas)

        except Exception as error:
            messagebox.showerror("Error", str(error))

    def cargar_tablas_en_combo():
        try:
            _, filas = listar_tablas()
            nombres_tablas = [fila[0] for fila in filas]
            combo_tabla["values"] = nombres_tablas

            if nombres_tablas and not tabla_var.get():
                tabla_var.set(nombres_tablas[0])

            status_var.set("Tablas cargadas correctamente.")

        except Exception:
            status_var.set("No se pudieron cargar las tablas. Revisa la conexion.")


    frame_reportes = ttk.LabelFrame(main_frame, text="Reportes automaticos", padding=10)
    frame_reportes.pack(fill=tk.X, pady=(0, 10))

    botones = [
        ("Probar conexion", test_connection),
        ("Total de tablas", cantidad_total_tablas),
        ("1. Listar tablas", listar_tablas),
        ("1. Listar indices", listar_indices),
        ("2. Indices por tabla", cantidad_indices_por_tabla),
        ("3. Restricciones", listar_restricciones),
        ("4. Detalle de indices", detalle_indices),
        ("5. Triggers", listar_triggers),
        ("6. Tamano tablas", tamano_tablas),
        ("7. Tamano registros", tamano_registros_todas_tablas),
        ("8. Tamano columnas", tamano_columnas),
        ("9. Factor bloqueo tablas", factor_bloqueo_todas_tablas),
        ("9. Factor bloqueo indices", factor_bloqueo_indices)
    ]

    for index, (texto, funcion) in enumerate(botones):
        fila = index // 4
        columna = index % 4

        boton = ttk.Button(
            frame_reportes,
            text=texto,
            command=lambda f=funcion: ejecutar_reporte(f)
        )

        boton.grid(row=fila, column=columna, padx=5, pady=5, sticky="ew")

    for columna in range(4):
        frame_reportes.columnconfigure(columna, weight=1)


    frame_parametros = ttk.LabelFrame(main_frame, text="Consultas con parametros", padding=10)
    frame_parametros.pack(fill=tk.X, pady=(0, 10))

    tabla_var = tk.StringVar()
    columna_var = tk.StringVar()

    lbl_tabla = ttk.Label(frame_parametros, text="Tabla:")
    lbl_tabla.grid(row=0, column=0, padx=5, pady=5, sticky="w")

    combo_tabla = ttk.Combobox(
        frame_parametros,
        textvariable=tabla_var,
        width=35
    )
    combo_tabla.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

    lbl_columna = ttk.Label(frame_parametros, text="Columna:")
    lbl_columna.grid(row=0, column=2, padx=5, pady=5, sticky="w")

    entry_columna = ttk.Entry(
        frame_parametros,
        textvariable=columna_var,
        width=35
    )
    entry_columna.grid(row=0, column=3, padx=5, pady=5, sticky="ew")

    btn_refrescar = ttk.Button(
        frame_parametros,
        text="Refrescar tablas",
        command=cargar_tablas_en_combo
    )
    btn_refrescar.grid(row=0, column=4, padx=5, pady=5, sticky="ew")

    btn_tamano_registro = ttk.Button(
        frame_parametros,
        text="Calcular tamano registro",
        command=ejecutar_tamano_registro
    )
    btn_tamano_registro.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

    btn_factor_tabla = ttk.Button(
        frame_parametros,
        text="Calcular factor bloqueo tabla",
        command=ejecutar_factor_bloqueo_tabla
    )
    btn_factor_tabla.grid(row=1, column=2, padx=5, pady=5, sticky="ew")

    btn_costo = ttk.Button(
        frame_parametros,
        text="10. Calcular costo igualdad",
        command=ejecutar_costo_igualdad
    )
    btn_costo.grid(row=1, column=3, padx=5, pady=5, sticky="ew")

    for columna in range(5):
        frame_parametros.columnconfigure(columna, weight=1)


    frame_resultados = ttk.LabelFrame(main_frame, text="Resultados", padding=10)
    frame_resultados.pack(fill=tk.BOTH, expand=True)

    tree = ttk.Treeview(frame_resultados)

    scroll_y = ttk.Scrollbar(
        frame_resultados,
        orient=tk.VERTICAL,
        command=tree.yview
    )

    scroll_x = ttk.Scrollbar(
        frame_resultados,
        orient=tk.HORIZONTAL,
        command=tree.xview
    )

    tree.configure(
        yscrollcommand=scroll_y.set,
        xscrollcommand=scroll_x.set
    )

    tree.grid(row=0, column=0, sticky="nsew")
    scroll_y.grid(row=0, column=1, sticky="ns")
    scroll_x.grid(row=1, column=0, sticky="ew")

    frame_resultados.rowconfigure(0, weight=1)
    frame_resultados.columnconfigure(0, weight=1)

    lbl_status = ttk.Label(
        main_frame,
        textvariable=status_var
    )
    lbl_status.pack(anchor="w", pady=(5, 0))

    cargar_tablas_en_combo()

    ventana.mainloop()