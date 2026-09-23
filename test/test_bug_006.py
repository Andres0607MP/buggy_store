import pytest
from main import TiendaOnline


def test_bug_006_inventarios_independientes():
    """Bug 6: Verifica que cada tienda tiene su propio inventario (argumento mutable por defecto)."""
    tienda1 = TiendaOnline()
    tienda1.agregar_producto("P01", "Teclado", 150000, 5)

    tienda2 = TiendaOnline()

    assert "P01" in tienda1.inventario
    assert tienda2.inventario == {}