from tkinter import Frame, Text, FLAT

class PanelRecibo:
    def __init__(self, panel, texto):
        self.panel = panel
        self.texto = texto


def crear_panel_recibo(parent):
    panel = Frame(parent, bd=1, relief=FLAT, bg='burlywood')
    panel.pack()

    texto = Text(
        panel,
        font=('Dosis', 12, 'bold'),
        bd=1,
        width=52,
        height=10,
    )
    texto.grid(row=0, column=0)

    return PanelRecibo(panel, texto)