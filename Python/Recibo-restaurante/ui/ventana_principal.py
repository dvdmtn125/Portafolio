from tkinter import Tk, Frame, Label, TOP, LEFT, RIGHT, FLAT

class VentanaPrincipal:
    def __init__(self, aplicacion, panel_izquierdo, panel_derecho):
        self.aplicacion = aplicacion
        self.panel_izquierdo = panel_izquierdo
        self.panel_derecho = panel_derecho

def crear_ventana_principal():
    aplicacion = Tk()
    aplicacion.geometry('1150x630+0+0')
    aplicacion.resizable(0, 0)
    aplicacion.title("Mi restaurante - Sistema de Facturación")
    aplicacion.config(bg='burlywood')

    panel_superior = Frame(aplicacion, bd=1, relief=FLAT)
    panel_superior.pack(side=TOP)

    etiqueta_titulo = Label(
        panel_superior,
        text='Sistema de Facturación',
        fg='azure4',
        font=('Dosis', 48),
        bg='burlywood',
        width=30,
    )
    etiqueta_titulo.grid(row=0, column=0)

    panel_izquierdo = Frame(aplicacion, bd=1, relief=FLAT)
    panel_izquierdo.pack(side=LEFT)

    panel_derecho = Frame(aplicacion, bd=1, relief=FLAT)
    panel_derecho.pack(side=RIGHT)

    return VentanaPrincipal(aplicacion, panel_izquierdo, panel_derecho)