import tkinter as tk
from tkinter import ttk

from ui.theme import COLORS, FONT_FAMILY


def mostrar_detalle(titulo, contenido, ventana_padre):
    ventana = tk.Toplevel(ventana_padre)
    ventana.title(titulo)
    ventana.geometry("720x420")
    ventana.minsize(480, 280)
    ventana.transient(ventana_padre)
    ventana.grab_set()

    marco = ttk.Frame(ventana, padding=16)
    marco.pack(fill=tk.BOTH, expand=True)

    ttk.Label(marco, text=titulo, style="Section.TLabel").pack(anchor="w", pady=(0, 10))

    texto = tk.Text(
        marco,
        wrap=tk.WORD,
        font=("Consolas", 10),
        bg="#F8FAFC",
        fg=COLORS["text"],
        relief="flat",
        padx=12,
        pady=12,
    )
    texto.pack(fill=tk.BOTH, expand=True)
    texto.insert("1.0", contenido)
    texto.configure(state="disabled")

    ttk.Button(
        marco,
        text="Cerrar",
        style="Primary.TButton",
        command=ventana.destroy,
    ).pack(anchor="e", pady=(12, 0))

    ventana.focus_set()
