import re

_CARACTERES_PERMITIDOS = re.compile(r'^[0-9+\-*/.\s]+$')


class Calculadora:
    def __init__(self):
        self._operador = ''

    @property
    def expresion_actual(self):
        return self._operador
    
    def agregar(self, texto):
        self._operador += texto
        return self._operador
    
    def borrar(self):
        self._operador =''
        return self._operador
    
    def calcular(self):
        expresion = self._operador

        if not expresion:
            raise ValueError('No hay ninguna operación para calcular')
        
        if not _CARACTERES_PERMITIDOS.match(expresion):
            raise ValueError(f"Expresión inválida: '{expresion}'")
        
        try:
            resultado = eval(expresion)
        except (SyntaxError, ZeroDivisionError) as error:
            raise ValueError(f"No se pudo calcular '{expresion}': {error}") from error
        self._operador = ''
        return str(resultado)