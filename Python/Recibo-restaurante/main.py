from data.productos import obtener_catalogo
from domain.calculadora import Calculadora

from ui.ventana_principal import crear_ventana_principal
from ui.panel_costos import crear_panel_costos
from ui.panel_productos import crear_panel_productos
from ui.panel_calculadora import crear_panel_calculadora
from ui.panel_recibo import crear_panel_recibo
from ui.panel_botones import crear_panel_botones

from controllers.controlador_facturacion import ControladorFacturacion
from controllers.controlador_calculadora import ControladorCalculadora


def main():
    ventana = crear_ventana_principal()


    panel_costos = crear_panel_costos(ventana.panel_izquierdo)

    catalogo = obtener_catalogo()


    controlador_facturacion = None

    productos = crear_panel_productos(
        ventana.panel_izquierdo,
        catalogo,
        lambda: controlador_facturacion.revisar_check(),
    )

    calculadora = Calculadora()
    controlador_calculadora = None  # mismo truco que arriba

    panel_calc = crear_panel_calculadora(
        ventana.panel_derecho,
        lambda simbolo: controlador_calculadora.agregar(simbolo),
        lambda: controlador_calculadora.calcular(),
        lambda: controlador_calculadora.borrar(),
    )
    controlador_calculadora = ControladorCalculadora(calculadora, panel_calc.visor)

    panel_recibo = crear_panel_recibo(ventana.panel_derecho)

    controlador_facturacion = ControladorFacturacion(
        productos,
        panel_costos.variables,
        panel_recibo.texto,
    )

    crear_panel_botones(
        ventana.panel_derecho,
        controlador_facturacion.calcular_total,
        controlador_facturacion.generar_recibo,
        controlador_facturacion.guardar,
        controlador_facturacion.resetear,
    )

    ventana.aplicacion.mainloop()


if __name__ == '__main__':
    main()