from tkinter import Frame, Button, FLAT

class PanelBotones:
    def __init__(self, panel, botones):
        self.panel = panel
        self.botones = botones

def crear_panel_botones(parent, al_total, al_recibo, al_guardar, al_resetear):
    panel = Frame(parent, bd=1, relief=FLAT, bg='burlywood')
    panel.pack()

    disposicion = [
        ('Total', al_total),
        ('Recibo', al_recibo),
        ('Guardar', al_guardar),
        ('Resetear', al_resetear),
    ]

    botones = []
    for columna, (texto, comando) in enumerate(disposicion):
        boton = Button(
            panel,
            text=texto,
            font=('Dosis', 14, 'bold'),
            fg='white',
            bg='azure4',
            bd=1,
            width=9,
            command=comando,
        )
        boton.grid(row=0, column=columna)
        botones.append(boton)

    return PanelBotones(panel, botones)