from tkinter import ttk

COLORS = {
    "bg": "#F1F5F9",
    "sidebar": "#0F172A",
    "sidebar_hover": "#1E293B",
    "sidebar_active": "#2563EB",
    "card": "#FFFFFF",
    "text": "#0F172A",
    "text_muted": "#64748B",
    "border": "#E2E8F0",
    "accent": "#2563EB",
    "accent_soft": "#DBEAFE",
    "success": "#059669",
    "danger": "#DC2626",
}

FONT_FAMILY = "Segoe UI"


def configurar_estilos():
    style = ttk.Style()
    style.theme_use("clam")

    style.configure(".", background=COLORS["bg"], foreground=COLORS["text"], font=(FONT_FAMILY, 10))
    style.configure("TFrame", background=COLORS["bg"])
    style.configure("Card.TFrame", background=COLORS["card"])
    style.configure("TLabel", background=COLORS["bg"], foreground=COLORS["text"])
    style.configure("Card.TLabel", background=COLORS["card"], foreground=COLORS["text"])
    style.configure("Muted.TLabel", background=COLORS["bg"], foreground=COLORS["text_muted"])
    style.configure("CardMuted.TLabel", background=COLORS["card"], foreground=COLORS["text_muted"])
    style.configure("Title.TLabel", font=(FONT_FAMILY, 20, "bold"), foreground=COLORS["text"])
    style.configure("Section.TLabel", font=(FONT_FAMILY, 13, "bold"), foreground=COLORS["text"])
    style.configure("CardTitle.TLabel", font=(FONT_FAMILY, 11, "bold"), background=COLORS["card"])

    style.configure(
        "Primary.TButton",
        font=(FONT_FAMILY, 10),
        padding=(14, 8),
        background=COLORS["accent"],
        foreground="#FFFFFF",
        borderwidth=0,
    )
    style.map(
        "Primary.TButton",
        background=[("active", "#1D4ED8"), ("pressed", "#1E40AF")],
        foreground=[("disabled", "#94A3B8")],
    )

    style.configure(
        "Secondary.TButton",
        font=(FONT_FAMILY, 10),
        padding=(12, 7),
        background=COLORS["card"],
        foreground=COLORS["text"],
        borderwidth=1,
        relief="solid",
    )
    style.map(
        "Secondary.TButton",
        background=[("active", COLORS["accent_soft"])],
    )

    style.configure(
        "Nav.TButton",
        font=(FONT_FAMILY, 10),
        padding=(16, 12),
        background=COLORS["sidebar"],
        foreground="#CBD5E1",
        borderwidth=0,
        anchor="w",
    )
    style.map(
        "Nav.TButton",
        background=[("active", COLORS["sidebar_hover"])],
        foreground=[("active", "#F8FAFC")],
    )

    style.configure(
        "NavActive.TButton",
        font=(FONT_FAMILY, 10, "bold"),
        padding=(16, 12),
        background=COLORS["sidebar_active"],
        foreground="#FFFFFF",
        borderwidth=0,
        anchor="w",
    )
    style.map(
        "NavActive.TButton",
        background=[("active", "#1D4ED8")],
        foreground=[("active", "#FFFFFF")],
    )

    style.configure(
        "Treeview",
        font=(FONT_FAMILY, 10),
        rowheight=28,
        background=COLORS["card"],
        fieldbackground=COLORS["card"],
        borderwidth=0,
    )
    style.configure(
        "Treeview.Heading",
        font=(FONT_FAMILY, 10, "bold"),
        background="#F8FAFC",
        foreground=COLORS["text"],
        relief="flat",
    )
    style.map(
        "Treeview",
        background=[("selected", COLORS["accent_soft"])],
        foreground=[("selected", COLORS["text"])],
    )

    style.configure(
        "Modern.TCombobox",
        font=(FONT_FAMILY, 10),
        padding=(10, 8),
        fieldbackground="#F8FAFC",
        background="#F8FAFC",
        foreground=COLORS["text"],
        borderwidth=0,
        relief="flat",
        arrowcolor=COLORS["text_muted"],
    )
    style.map(
        "Modern.TCombobox",
        fieldbackground=[("readonly", "#F8FAFC"), ("disabled", "#F8FAFC")],
        foreground=[("disabled", COLORS["text_muted"])],
        arrowcolor=[("disabled", "#CBD5E1")],
    )

    style.layout(
        "Modern.TCombobox",
        [
            (
                "Combobox.field",
                {
                    "sticky": "nswe",
                    "children": [
                        (
                            "Combobox.padding",
                            {
                                "expand": "1",
                                "sticky": "nswe",
                                "children": [
                                    ("Combobox.textarea", {"sticky": "nswe"}),
                                ],
                            },
                        )
                    ],
                },
            ),
            ("Combobox.downarrow", {"side": "right", "sticky": "ns"}),
        ],
    )
