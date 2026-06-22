import tkinter as tk

from ui.icons import FONT_MDL2
from ui.theme import COLORS, FONT_FAMILY

_VARIANTS = {
    "nav": {
        "bg": COLORS["sidebar"],
        "fg": "#CBD5E1",
        "icon_fg": "#94A3B8",
        "hover_bg": COLORS["sidebar_hover"],
        "font": (FONT_FAMILY, 10),
        "padx": 16,
        "pady": 12,
    },
    "nav_active": {
        "bg": COLORS["sidebar_active"],
        "fg": "#FFFFFF",
        "icon_fg": "#FFFFFF",
        "hover_bg": "#1D4ED8",
        "font": (FONT_FAMILY, 10, "bold"),
        "padx": 16,
        "pady": 12,
    },
    "primary": {
        "bg": COLORS["accent"],
        "fg": "#FFFFFF",
        "icon_fg": "#FFFFFF",
        "hover_bg": "#1D4ED8",
        "font": (FONT_FAMILY, 10),
        "padx": 14,
        "pady": 8,
    },
    "secondary": {
        "bg": COLORS["card"],
        "fg": COLORS["text"],
        "icon_fg": COLORS["accent"],
        "hover_bg": COLORS["accent_soft"],
        "font": (FONT_FAMILY, 10),
        "padx": 12,
        "pady": 7,
        "border": COLORS["border"],
    },
}


class IconButton(tk.Frame):
    def __init__(self, padre, icono, texto, comando, variant="secondary"):
        self._variant = variant
        self._comando = comando
        self._estilo = _VARIANTS[variant]

        super().__init__(padre, bg=self._estilo["bg"], cursor="hand2")

        if variant == "secondary" and "border" in self._estilo:
            self.configure(
                highlightthickness=1,
                highlightbackground=self._estilo["border"],
                highlightcolor=self._estilo["border"],
            )

        self._icon = tk.Label(
            self,
            text=icono,
            font=(FONT_MDL2, 11),
            bg=self._estilo["bg"],
            fg=self._estilo["icon_fg"],
        )
        self._icon.pack(side=tk.LEFT, padx=(self._estilo["padx"], 8))

        self._label = tk.Label(
            self,
            text=texto,
            font=self._estilo["font"],
            bg=self._estilo["bg"],
            fg=self._estilo["fg"],
        )
        self._label.pack(side=tk.LEFT, padx=(0, self._estilo["padx"]), pady=self._estilo["pady"])

        for widget in (self, self._icon, self._label):
            widget.bind("<Button-1>", self._on_click)
            widget.bind("<Enter>", self._on_enter)
            widget.bind("<Leave>", self._on_leave)

    def _on_click(self, _event):
        if self._comando:
            self._comando()
        self.winfo_toplevel().focus_set()

    def _on_enter(self, _event):
        bg = self._estilo["hover_bg"]
        self._aplicar_color(bg)

    def _on_leave(self, _event):
        self._aplicar_color(self._estilo["bg"])

    def _aplicar_color(self, bg):
        self.configure(bg=bg)
        self._icon.configure(bg=bg)
        self._label.configure(bg=bg)

    def set_variant(self, variant):
        self._variant = variant
        self._estilo = _VARIANTS[variant]
        self._aplicar_color(self._estilo["bg"])
        self._icon.configure(fg=self._estilo["icon_fg"])
        self._label.configure(fg=self._estilo["fg"], font=self._estilo["font"])
