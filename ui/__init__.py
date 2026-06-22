import tkinter as tk
from tkinter import messagebox

from init_db import ensure_initialized
from ui.app import StreamUCVApp


def _mensaje_error_conexion(error):
    texto = str(error)
    if "18456" in texto or "Login failed" in texto:
        return (
            "No se pudo conectar a SQL Server.\n\n"
            "Revisa config.py:\n"
            "- USE_WINDOWS_AUTH = True para tu cuenta Windows\n"
            "- USE_WINDOWS_AUTH = False y ajusta USERNAME/PASSWORD si usas SQL auth\n\n"
            f"Detalle tecnico: {texto}"
        )
    return texto


def iniciar_app():
    ventana = tk.Tk()
    ventana.withdraw()

    try:
        acciones = ensure_initialized()
        if acciones:
            messagebox.showinfo(
                "Base de datos inicializada",
                "Se crearon los siguientes elementos:\n\n"
                + "\n".join(f"- {accion}" for accion in acciones),
            )
    except Exception as error:
        messagebox.showerror(
            "Error al inicializar la base de datos",
            _mensaje_error_conexion(error),
        )
        ventana.destroy()
        return

    ventana.deiconify()
    ventana.title("StreamUCV — Diccionario de Datos")
    ventana.geometry("1280x780")
    ventana.minsize(1024, 680)

    StreamUCVApp(ventana)
    ventana.mainloop()
