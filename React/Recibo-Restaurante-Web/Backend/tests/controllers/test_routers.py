def test_crear_y_listar_categoria(cliente):
    respuesta_crear = cliente.post('/categorias/', json={'nombre': 'Bebidas'})
    assert respuesta_crear.status_code == 201
    categoria_id = respuesta_crear.json()['id']

    respuesta_listar = cliente.get('/categorias/')
    assert respuesta_listar.status_code == 200
    assert len(respuesta_listar.json()) == 1
    assert respuesta_listar.json()[0]['id'] == categoria_id


def test_crear_categoria_nombre_vacio_devuelve_400(cliente):
    respuesta = cliente.post('/categorias/', json={'nombre': ''})
    assert respuesta.status_code == 400


def test_eliminar_categoria_con_productos_devuelve_409(cliente):
    categoria_id = cliente.post('/categorias/', json={'nombre': 'Bebidas'}).json()['id']
    cliente.post('/productos/', json={'nombre': 'Limonada', 'precio': 5000, 'categoria_id': categoria_id})

    respuesta = cliente.delete(f'/categorias/{categoria_id}')

    assert respuesta.status_code == 409


def test_crear_producto_con_categoria_inexistente_devuelve_400(cliente):
    respuesta = cliente.post('/productos/', json={'nombre': 'Limonada', 'precio': 5000, 'categoria_id': 999})
    assert respuesta.status_code == 400


def test_actualizar_producto_devuelve_200_con_datos_nuevos(cliente):
    categoria_id = cliente.post('/categorias/', json={'nombre': 'Bebidas'}).json()['id']
    producto_id = cliente.post(
        '/productos/', json={'nombre': 'Limonada', 'precio': 5000, 'categoria_id': categoria_id}
    ).json()['id']

    respuesta = cliente.put(
        f'/productos/{producto_id}',
        json={'nombre': 'Limonada Grande', 'precio': 7000, 'categoria_id': categoria_id},
    )

    assert respuesta.status_code == 200
    assert respuesta.json()['precio'] == 7000


def test_eliminar_producto_devuelve_204(cliente):
    categoria_id = cliente.post('/categorias/', json={'nombre': 'Bebidas'}).json()['id']
    producto_id = cliente.post(
        '/productos/', json={'nombre': 'Limonada', 'precio': 5000, 'categoria_id': categoria_id}
    ).json()['id']

    respuesta = cliente.delete(f'/productos/{producto_id}')

    assert respuesta.status_code == 204


def test_calcular_factura_devuelve_totales(cliente):
    respuesta = cliente.post(
        '/facturacion/calcular',
        json={'cantidades': {'comida': [2]}, 'precios': {'comida': [15000]}},
    )

    assert respuesta.status_code == 200
    assert respuesta.json()['subtotal'] == 30000


def test_generar_recibo_devuelve_texto(cliente):
    respuesta = cliente.post(
        '/facturacion/recibo',
        json={
            'items': {'comida': [['Bandeja Paisa', 2, 15000]]},
            'calculo': {'comida': 30000, 'bebida': 0, 'postres': 0, 'subtotal': 30000, 'iva': 5700, 'total': 35700},
        },
    )

    assert respuesta.status_code == 200
    assert 'Bandeja Paisa' in respuesta.json()['recibo']