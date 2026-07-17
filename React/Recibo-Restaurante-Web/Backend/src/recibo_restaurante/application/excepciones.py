class CategoriaConProductosAsociadosError(Exception):
    """Se lanza al intentar eliminar una categoría que todavía tiene productos."""
    def __init__(self, categoria_id: int, cantidad_productos: int) -> None:
        self.categoria_id = categoria_id
        self.cantidad_productos = cantidad_productos
        super().__init__(
            f'No se puede eliminar la categoria {categoria_id}: '
            f'tiene {cantidad_productos} producto(s) asociado(s).'
        )