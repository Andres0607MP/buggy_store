import pytest
from main import TiendaOnline


def _setup_tienda():
    """Crea una TiendaOnline con estado limpio para aislar Bug 004.
    
    Workarounds para bugs originales que interfieren:
    - Bug 001/006 (mutable default): pasar dict nuevo explícitamente.
    - Typo ventas_totaIes (línea 37): inicializar el atributo.
    """
    tienda = TiendaOnline({})
    tienda.ventas_totaIes = 0.0
    return tienda


def test_bug_004_compra_dentro_del_stock():
    """Compra una cantidad menor al stock disponible."""
    tienda = _setup_tienda()
    tienda.agregar_producto("P01", "Teclado", 150000, 5)

    carrito = [{"id_producto": "P01", "cantidad": 2}]
    total = tienda.procesar_pedido(carrito)

    assert tienda.inventario["P01"]["cantidad"] == 3
    assert total == 300000


def test_bug_004_compra_exactamente_el_stock():
    """Compra exactamente todo el stock disponible."""
    tienda = _setup_tienda()
    tienda.agregar_producto("P01", "Teclado", 150000, 5)

    carrito = [{"id_producto": "P01", "cantidad": 5}]
    total = tienda.procesar_pedido(carrito)

    assert tienda.inventario["P01"]["cantidad"] == 0
    assert total == 750000


def test_bug_004_compra_superior_al_stock():
    """Solicita más unidades de las disponibles.
    
    El item debe ignorarse: stock no cambia y no se suma al total.
    """
    tienda = _setup_tienda()
    tienda.agregar_producto("P01", "Teclado", 150000, 5)

    carrito = [{"id_producto": "P01", "cantidad": 10}]
    total = tienda.procesar_pedido(carrito)

    assert tienda.inventario["P01"]["cantidad"] == 5  # Sin cambios
    assert total == 0  # No se incluyó
    assert tienda.inventario["P01"]["cantidad"] >= 0  # No negativo


def test_bug_004_nunca_stock_negativo():
    """Verifica que el inventario nunca tenga cantidades negativas."""
    tienda = _setup_tienda()
    tienda.agregar_producto("P01", "Teclado", 150000, 3)
    tienda.agregar_producto("P02", "Mouse", 80000, 2)

    carrito = [
        {"id_producto": "P01", "cantidad": 10},  # excesivo → ignora
        {"id_producto": "P02", "cantidad": 5},   # excesivo → ignora
    ]
    tienda.procesar_pedido(carrito)

    assert tienda.inventario["P01"]["cantidad"] == 3
    assert tienda.inventario["P02"]["cantidad"] == 2

    # Todos los productos con cantidad >= 0
    for prod_id in tienda.inventario:
        assert tienda.inventario[prod_id]["cantidad"] >= 0