from tkinter import ttk

from ui.theme import FONT_FAMILY


class ModernCombobox:
    def __init__(self, padre, textvariable, width=28, on_change=None):
        self.combo = ttk.Combobox(
            padre,
            textvariable=textvariable,
            width=width,
            state="readonly",
            style="Modern.TCombobox",
            font=(FONT_FAMILY, 10),
        )

        if on_change:
            self.combo.bind("<<ComboboxSelected>>", lambda _event: on_change())

    def set_values(self, values):
        self.combo["values"] = values

    def grid(self, **kwargs):
        self.combo.grid(**kwargs)

    def pack(self, **kwargs):
        self.combo.pack(**kwargs)

    def bind(self, sequence, callback):
        self.combo.bind(sequence, callback)
