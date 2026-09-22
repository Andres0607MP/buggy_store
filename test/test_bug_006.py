from main import TiendaOnline


def test_inventarios_independientes():
    tienda1 = TiendaOnline()
    tienda1.agregar_producto("P01", "Teclado", 150000, 5)

    tienda2 = TiendaOnline()

    assert "P01" in tienda1.inventario
    assert tienda2.inventario == {}