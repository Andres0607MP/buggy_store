from main import TiendaOnline


def test_cupon_aplica_descuento_del_20_por_ciento():
    tienda = TiendaOnline()
    tienda.agregar_producto("P01", "Teclado", 100000, 5)

    total = tienda.procesar_pedido(
        [{"id_producto": "P01", "cantidad": 1}],
        cupon_descuento="SENA2026"
    )

    assert total == 80000