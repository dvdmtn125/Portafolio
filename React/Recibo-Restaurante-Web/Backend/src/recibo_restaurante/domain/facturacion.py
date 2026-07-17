IVA_PORCENTAJE = 0.19


def calcular_subtotal(cantidades: list[float], precios: list[float]) -> float:
    if len(cantidades) != len(precios):
        raise ValueError(
            f"Cantidades ({len(cantidades)}) y precios ({len(precios)})"
            "no coinciden en longitud."
        )
    return sum(cantidad * precio for cantidad, precio in zip(cantidades, precios))

def calcular_totales(
        cantidades: dict[str, list[float]],
        precios: dict[str, list[float]],
        ) -> dict[str, float]:
    if cantidades.keys() != precios.keys():
        raise ValueError(
            f"Las categorias de cantidad ({list(cantidades)}) no coinciden "
            f"con los precios ({list(precios)})."
        )
    
    subtotales_por_categoria = {
        categoria: calcular_subtotal(cantidades[categoria], precios[categoria])
        for categoria in cantidades
    }

    subtotal = sum(subtotales_por_categoria.values())
    iva = subtotal * IVA_PORCENTAJE
    total = subtotal + iva

    resultado = {
        categoria: round(valor, 2)
        for categoria, valor in subtotales_por_categoria.items()
    }
    resultado['subtotal'] = round(subtotal, 2)
    resultado['iva'] = round(iva, 2)
    resultado['total'] = round(total, 2)
    return resultado