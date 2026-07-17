from recibo_restaurante.domain import facturacion


class CalcularFactura:
    def ejecutar(
            self,
            cantidades: dict[str, list[float]],
            precios: dict[str, list[float]],
    ) -> dict[str, float]:
        return facturacion.calcular_totales(cantidades, precios)