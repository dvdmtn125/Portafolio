from tkinter import (
    LabelFrame,
    Checkbutton,
    Entry,
    IntVar,
    StringVar,
    DISABLED,
    W,
    LEFT,
    FLAT)

_TITULOS = {
    'comida' : 'Comida',
    'bebida' : 'Bebidas',
    'postres' : 'Postres',
}


def crear_panel_productos(parent, catalogo, al_cambiar_seleccion):
    productos = {}

    for categoria, datos in catalogo.items():
        panel = LabelFrame(
            parent,
            text=_TITULOS.get(categoria, categoria.title()),
            font=('Dosis', 19, 'bold'),
            bd=1,
            relief=FLAT,
            fg='azure4',
        )
        panel.pack(side=LEFT)

        variables = []
        cantidades = []
        entradas = []

        for fila, nombre in enumerate(datos['nombres']):
            variable = IntVar()
            variables.append(variable)

            checkbox = Checkbutton(
                panel,
                text=nombre.title(),
                font=('Dosis', 19, 'bold'),
                onvalue=1,
                offvalue=0,
                variable=variable,
                command=al_cambiar_seleccion,
            )
            checkbox.grid(row=fila, column=0, sticky=W)

            cantidad = StringVar()
            cantidad.set('0')
            cantidades.append(cantidad)

            entrada = Entry(
                panel,
                font=('Dosis', 18, 'bold'),
                bd=1,
                width=6,
                state=DISABLED,
                textvariable=cantidad,
            )
            entrada.grid(row=fila, column=1)
            entradas.append(entrada)

        productos[categoria] = {
            'nombres': datos['nombres'],
            'precios': datos['precios'],
            'variables': variables,
            'cantidades': cantidades,
            'entradas': entradas,
        }

    return productos