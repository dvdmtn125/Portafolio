from tkinter import END

class ControladorCalculadora:
    def __init__(self, calculadora, visor):
        self.calculadora = calculadora
        self.visor = visor

    def _refrescar_visor(self, texto):
        self.visor.delete(0, END)
        self.visor.insert(0, texto)

    def agregar(self, simbolo):
        expresion = self.calculadora.agregar(simbolo)
        self._refrescar_visor(expresion)

    def borrar(self):
        expresion = self.calculadora.borrar()
        self._refrescar_visor(expresion)

    def calcular(self):
        try:
            resultado = self.calculadora.calcular()
        except ValueError:
            resultado = 'Error'
            self.calculadora.borrar()

        self._refrescar_visor(resultado)