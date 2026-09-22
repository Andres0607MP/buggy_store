import pytest
from main import TiendaOnline


def _setup_tienda():
    """Crea una TiendaOnline con estado limpio y el atributo ventas_totaIes inicializado.
    
    Workarounds para bugs originales que interfieren con probar Bug 003:
    
    1. Bug 001 (mutable default argument): Pasamos un dict nuevo explícitamente para
       evitar que todas las instancias compartan el mismo inventario.
    2. Typo en línea 40 (ventas_totaIes en lugar de ventas_totales): Inicializamos
       el atributo con el nombre erróneo para que procesar_pedido pueda completarse.
    
    Estos workarounds NO modifican el código de producción, solo permiten aislar
    la prueba del Bug 003.
    """
    tienda = TiendaOnline({})
    tienda.ventas_totaIes = 0.0
    return tienda


def test_bug_003_product_exists_processed_correctly():
    """Verifica que un producto existente en el inventario se procese sin error."""
    tienda = _setup_tienda()
    tienda.agregar_producto("P01", "Teclado", 150000, 5)

    carrito = [{"id_producto": "P01", "cantidad": 2}]

    total = tienda.procesar_pedido(carrito)

    assert total == 300000
    assert tienda.inventario["P01"]["cantidad"] == 3


def test_bug_003_product_not_exists_no_KeyError():
    """Verifica que un producto inexistente no lance KeyError."""
    tienda = _setup_tienda()
    tienda.agregar_producto("P01", "Teclado", 150000, 5)

    carrito = [{"id_producto": "INEXISTENTE", "cantidad": 1}]

    total = tienda.procesar_pedido(carrito)

    assert total == 0


def test_bug_003_product_not_exists_no_inventory_change():
    """Verifica que un producto inexistente no agregue ni modifique el inventario."""
    tienda = _setup_tienda()
    tienda.agregar_producto("P01", "Teclado", 150000, 5)

    inventario_inicial = dict(tienda.inventario)

    carrito = [{"id_producto": "INEXISTENTE", "cantidad": 1}]
    tienda.procesar_pedido(carrito)

    assert tienda.inventario == inventario_inicial


def test_bug_003_valid_then_invalid_in_carrito():
    """Verifica que un producto válido se procese y el inexistente se ignore."""
    tienda = _setup_tienda()
    tienda.agregar_producto("P01", "Teclado", 150000, 5)

    carrito = [
        {"id_producto": "P01", "cantidad": 2},
        {"id_producto": "INEXISTENTE", "cantidad": 1},
    ]

    total = tienda.procesar_pedido(carrito)

    assert total == 300000
    assert tienda.inventario["P01"]["cantidad"] == 3