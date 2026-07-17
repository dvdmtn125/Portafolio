from datetime import datetime

from recibo_restaurante.domain import recibo


class GenerarRecibo:
    def ejecutar(
            self,
            items: dict[str, list[tuple[str, float, float]]],
            calculo: dict[str, float],
            numero_recibo: str | None = None,
            fecha: datetime | None = None,
    ) -> str:
        items_normalizados = {
            categoria: [
                (nombre, str(cantidad), precio_unitario)
                for nombre, cantidad, precio_unitario in items_categoria
            ]
            for categoria, items_categoria in items.items()
        }
        return recibo.generar_recibo(items_normalizados, calculo, numero_recibo, fecha)