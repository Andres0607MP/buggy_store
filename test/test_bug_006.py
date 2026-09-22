import pytest
from main import TiendaOnline


def _setup_tienda():
    """Crea una TiendaOnline con estado limpio para aislar Bug 1.
    
    Workaround para Bug 6 (mutable default): pasar dict nuevo explícitamente.
    """
    tienda = TiendaOnline({})
    return tienda


def test_bug_001_ventas_totales_se_actualiza_sin_AttributeError():
    """Bug 1: procesar_pedido() debe ejecutarse sin AttributeError
    y actualizar self.ventas_totales correctamente.
    
    Verifica que el typo original 'ventas_totaIes' (con I mayúscula)
    fue corregido a 'ventas_totales' (con l minúscula).
    """
    tienda = _setup_tienda()
    tienda.agregar_producto("P01", "Teclado", 100000, 5)

    # Ejecutar un pedido simple SIN cupón
    total = tienda.procesar_pedido([{"id_producto": "P01", "cantidad": 1}])

    # 1. El método debe retornar el total sin lanzar AttributeError
    assert total == 100000

    # 2. El atributo correcto 'ventas_totales' debe existir y tener el valor correcto
    assert hasattr(tienda, "ventas_totales"), "Falta atributo 'ventas_totales'"
    assert tienda.ventas_totales == 100000, f"ventas_totales debería ser 100000, es {tienda.ventas_totales}"

    # 3. El atributo INCORRECTO 'ventas_totaIes' NO debe haberse creado/usado
    # (Si el bug existiera, ventas_totales sería 0 y ventas_totaIes existiría)
    assert not hasattr(tienda, "ventas_totaIes"), "El typo 'ventas_totaIes' no debería existir"


def test_bug_001_ventas_totales_acumula_multiples_pedidos():
    """Bug 1: ventas_totales debe acumularse correctamente en múltiples pedidos."""
    tienda = _setup_tienda()
    tienda.agregar_producto("P01", "Teclado", 100000, 10)
    tienda.agregar_producto("P02", "Mouse", 50000, 10)

    # Pedido 1
    total1 = tienda.procesar_pedido([{"id_producto": "P01", "cantidad": 2}])
    # Pedido 2
    total2 = tienda.procesar_pedido([{"id_producto": "P02", "cantidad": 1}])

    assert total1 == 200000
    assert total2 == 50000
    assert tienda.ventas_totales == 250000, f"ventas_totales debería acumular 250000, es {tienda.ventas_totales}"


def test_bug_001_con_cupon_descuento():
    """Bug 1: ventas_totales debe registrar el total YA CON DESCUENTO aplicado."""
    tienda = _setup_tienda()
    tienda.agregar_producto("P01", "Teclado", 100000, 5)

    total = tienda.procesar_pedido(
        [{"id_producto": "P01", "cantidad": 1}],
        cupon_descuento="SENA2026"
    )

    # Con descuento 20%, total = 80000
    assert total == 80000
    assert tienda.ventas_totales == 80000, "ventas_totales debe reflejar el total con descuento"