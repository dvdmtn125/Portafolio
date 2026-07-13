from tkinter import END, DISABLED, messagebox

from domain import facturacion, recibo
from infrastructure import almacenamiento


class ControladorFacturacion:
    def __init__(self, productos, widgets_costos, texto_recibo):
        self.productos = productos
        self.widgets_costos = widgets_costos
        self.texto_recibo = texto_recibo
        self._ultimo_calculo = None

    def revisar_check(self):
        for datos in self.productos.values():
            for i, variable in enumerate(datos['variables']):
                entrada = datos['entradas'][i]
                cantidad = datos['cantidades'][i]
                if variable.get() == 1:
                    entrada.config(state='normal')
                    if cantidad.get() == '0':
                        entrada.delete(0, END)
                    entrada.focus()
                else:
                    entrada.config(state=DISABLED)
                    cantidad.set('0')

    def calcular_total(self):
        cantidades = {
            categoria: [float(c.get()) for c in datos['cantidades']]
            for categoria, datos in self.productos.items()
        }
        precios = {
            categoria: datos['precios']
            for categoria, datos in self.productos.items()
        }

        resultado = facturacion.calcular_totales(cantidades, precios)
        self._ultimo_calculo = resultado

        self.widgets_costos['comida'].set(f"${resultado['comida']}")
        self.widgets_costos['bebida'].set(f"${resultado['bebida']}")
        self.widgets_costos['postres'].set(f"${resultado['postres']}")
        self.widgets_costos['subtotal'].set(f"${resultado['subtotal']}")
        self.widgets_costos['iva'].set(f"${resultado['iva']}")
        self.widgets_costos['total'].set(f"${resultado['total']}")

    def generar_recibo(self):
        if self._ultimo_calculo is None:
            self.calcular_total()

        items = {
            categoria: [
                (datos['nombres'][i], datos['cantidades'][i].get(), datos['precios'][i])
                for i in range(len(datos['nombres']))
            ]
            for categoria, datos in self.productos.items()
        }

        texto = recibo.generar_recibo(items, self._ultimo_calculo)

        self.texto_recibo.delete(1.0, END)
        self.texto_recibo.insert(END, texto)

    def guardar(self):
        contenido = self.texto_recibo.get(1.0,END)
        guardado = almacenamiento.guardar_recibo(contenido)
        if guardado:
            messagebox.showinfo('Información', 'Su recibo ha sido guardado.')
        
    def resetear(self):
        self.texto_recibo.delete(1.0, END)
        self._ultimo_calculo = None

        for datos in self.productos.values():
            for cantidad in datos['cantidades']:
                cantidad.set('0')
            for entrada in datos['entradas']:
                entrada.config(state=DISABLED)
            for variable in datos['variables']:
                variable.set(0)

        for var in self.widgets_costos.values():
            var.set('')
