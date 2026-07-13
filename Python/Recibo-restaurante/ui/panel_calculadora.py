from tkinter import Frame, Entry, Button, FLAT

_DISPOSICION_BOTONES = [
    ('7', '7'), ('8', '8'), ('9', '9'), ('+', '+'),
    ('4', '4'), ('5', '5'), ('6', '6'), ('-', '-'),
    ('1', '1'), ('2', '2'), ('3', '3'), ('x', '*'),
    ('R', 'CALCULAR'), ('B', 'BORRAR'), ('0', '0'), ('/', '/'),
]

_COLUMNAS = 4


class PanelCalculadora:
    def __init__(self, panel, visor):
        self.panel = panel
        self.visor = visor

def crear_panel_calculadora(parent, al_agregar, al_calcular, al_borrar):
    panel = Frame(parent, bd=1, relief=FLAT, bg='burlywood')
    panel.pack()

    visor = Entry(panel, font=('Dosis', 16, 'bold'), width=42, bd=1)
    visor.grid(row=0, column=0, columnspan=_COLUMNAS)

    for indice, (texto, accion) in enumerate(_DISPOSICION_BOTONES):
        boton = Button(
            panel,
            text=texto,
            font=('Dosis', 16, 'bold'),
            fg='white',
            bg='azure4',
            bd=1,
            width=9,
        )

        if accion == 'CALCULAR':
            boton.config(command=al_calcular)
        elif accion == 'BORRAR':
            boton.config(command=al_borrar)
        else:
            boton.config(command=lambda accion=accion: al_agregar(accion))

        fila = 1 + indice // _COLUMNAS
        columna = indice % _COLUMNAS
        boton.grid(row=fila, column=columna)

    return PanelCalculadora(panel, visor)
        