# Buggy Store

## Contexto

Acabamos de heredar el backend de una pequeña tienda en línea escrito por un desarrollador junior. El sistema permite registrar productos, procesar compras y limpiar el inventario. Sin embargo, los clientes se quejan de que los cobros son incorrectos, el inventario se daña y el sistema a veces colapsa. Su misión es encontrar y reparar los 6 bugs mortales escondidos en este código.

## Bugs corregidos

### Bug 1 — Typo en atributo de ventas

**Problema:** `ventas_totaIes`
**Causa:** `I` mayúscula en lugar de `l` minúscula.
**Comportamiento:** `AttributeError` al registrar una venta.
**Solución:** `self.ventas_totales += total_pedido`
**Archivo:** `main.py`
**Test real:** `test/test_bug_001.py` (3 tests)

---

### Bug 2 — Cupón que encarecía el pedido

**Problema:** multiplicación por `1.20`.
**Causa:** factor incorrecto para un descuento.
**Comportamiento:** aumentaba el total en 20%.
**Solución:** multiplicar por `0.80`.
**Archivo:** `main.py`
**Test real existente:** `test/test_bug_002.py` (1 test)

---

### Bug 3 — Producto inexistente en carrito

**Problema:** acceso directo a `self.inventario[id_prod]`.
**Causa:** no se validaba la existencia del producto.
**Comportamiento:** `KeyError`.
**Solución:** validar `id_prod not in self.inventario` y continuar.
**Archivo:** `main.py`
**Test:** `test/test_bug_003.py` (4 tests)

---

### Bug 4 — Stock insuficiente

**Problema:** permitía comprar más unidades que las disponibles.
**Causa:** ausencia de validación del stock.
**Comportamiento:** inventario podía quedar negativo.
**Solución:** validar `cant_comprada > producto['cantidad']` antes de descontar.
**Archivo:** `main.py`
**Test:** `test/test_bug_004.py` (4 tests)

---

### Bug 5 — RuntimeError al limpiar agotados

**Problema:** eliminar elementos del diccionario mientras se itera sobre sus claves.
**Causa:** modificación del diccionario durante la iteración.
**Comportamiento:** `RuntimeError: dictionary changed size during iteration`.
**Solución:** iterar sobre `list(self.inventario.keys())`.
**Archivo:** `main.py`
**Test real existente:** `test/test_bug_005.py` (1 test)

---

### Bug 6 — Argumento mutable por defecto

**Problema:** `inventario_inicial={}`.
**Causa:** los argumentos mutables por defecto se comparten entre instancias.
**Comportamiento:** diferentes tiendas podían compartir el mismo inventario.
**Solución:** `inventario_inicial=None` y crear un diccionario independiente cuando sea necesario.
**Archivo:** `main.py`
**Test real existente:** `test/test_bug_006.py` (1 test)

---

## Pruebas

Documenta los archivos REALES que existen actualmente:

* `test/test_bug_001.py` — Bug 1 — 3 tests
* `test/test_bug_002.py` — Bug 2 — 1 test
* `test/test_bug_003.py` — Bug 3 — 4 tests
* `test/test_bug_004.py` — Bug 4 — 4 tests
* `test/test_bug_005.py` — Bug 5 — 1 test
* `test/test_bug_006.py` — Bug 6 — 1 test

**Resultado esperado/actual:**
`14 passed`

Comando de ejecución:
```bash
python -m pytest -v
```

---

## Commits relevantes

* Bug 1 — `b81c7f0`
* Bug 2 — `95cf400`
* Bug 3 — `0a594dc`
* Bug 4 — `c9670db`
* Bug 5 — `f86b069`
* Bug 6 — `ce8f763`

Estos son commits históricos asociados a las correcciones y no se han reescrito.

---

## Estado final

* 6/6 bugs corregidos.
* 14/14 tests pasando.
* Código de producción funcional.
* `test/` contiene únicamente archivos de pruebas.
* La documentación explicativa está centralizada en el README principal.