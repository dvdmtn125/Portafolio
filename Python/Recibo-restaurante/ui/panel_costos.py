from tkinter import Frame, Label, Entry, StringVar, FLAT

_FILAS = [
    [('Costo Comida', 'comida'), ('Subtotal', 'subtotal')],
    [('Costo Bebida', 'bebida'), ('Iva', 'iva')],
    [('Costo Postres', 'postres'), ('Total', 'total')],
]


class PanelCostos:
    def __init__(self, panel, variables):
        self.panel = panel
        self.variables = variables

def crear_panel_costos(parent):
    panel = Frame(parent, bd=1, relief=FLAT, bg='azure4', padx=70)
    panel.pack(side='bottom')

    variables = {}

    for fila, pares in enumerate(_FILAS):
        for indice_par, (texto, llave) in enumerate(pares):
            variable = StringVar()
            variables[llave] = variable

            columna_etiqueta = indice_par * 2
            columna_entrada = columna_etiqueta + 1

            etiqueta = Label(
                panel,
                text=texto,
                font=('Dosis', 12, 'bold'),
                bg='azure4',
                fg='white',
            )
            etiqueta.grid(row=fila, column=columna_etiqueta)

            entrada = Entry(
                panel,
                font=('Dosis', 12, 'bold'),
                bd=1,
                width=10,
                state='readonly',
                textvariable=variable,
            )
            entrada.grid(row=fila, column=columna_entrada, padx=41)

    return PanelCostos(panel,  variables)