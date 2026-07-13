PRODUCTOS = {
    'comida': {
        'nombres': ['pollo', 'cordero', 'salmon', 'merluza', 'kebab', 'pizza1', 'pizza2', 'pizza3'],
        'precios': [1.32, 1.65, 2.31, 3.22, 1.22, 1.99, 2.05, 2.65],
    },
    'bebida': {
        'nombres': ['agua', 'soda', 'jugo', 'cola', 'vino1', 'vino2', 'cerveza1', 'cerveza2'],
        'precios': [0.25, 0.99, 1.21, 1.54, 1.08, 1.10, 2.00, 1.58],
    },
    'postres': {
        'nombres': ['helado', 'fruta', 'brownies', 'flan', 'mousse', 'pastel1', 'pastel2', 'pastel3'],
        'precios': [1.54, 1.68, 1.32, 1.97, 2.55, 2.14, 1.94, 1.74],
    },
}


def validar_catalogo(catalogo=PRODUCTOS):
    for categoria, datos in catalogo.items():
        if len(datos['nombres']) != len(datos['precios']):
            raise ValueError(
                f"'{categoria}': hay {len(datos['nombres'])} nombres "
                f"pero {len(datos['precios'])} precios."
            )
    return True

def obtener_catalogo():
    return {
        categoria: {
            'nombres': list(datos['nombres']),
            'precios': list(datos['precios']),
        }
        for categoria, datos in PRODUCTOS.items()
    }


validar_catalogo()