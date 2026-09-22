# Buggy Store

## Contexto

Acabamos de heredar el backend de una pequeña tienda en línea escrito por un desarrollador junior. El sistema permite registrar productos, procesar compras y limpiar el inventario, pero contiene varios errores.

Este trabajo documenta y corrige los 6 bugs oficiales.

---

## Bug 1: Typo en atributo de ventas (`ventas_totaIes` → `ventas_totales`)

### Error

En el método `procesar_pedido()`, al registrar la venta, se usaba un atributo con un typo:

```python
self.ventas_totaIes += total_pedido  # 'I' mayúscula en lugar de 'l' minúscula
```

El atributo correcto declarado en `__init__` es `self.ventas_totales`, por lo que el código lanzaba `AttributeError` al intentar completar un pedido.

### Causa

Error tipográfico: la letra "I" (i mayúscula) se usó en lugar de "l" (ele minúscula) en `ventas_totaIes`.

### Corrección

Se corrigió el nombre del atributo al correcto `ventas_totales`:

```python
self.ventas_totales += total_pedido
```

### Rama y test

- Rama: `bugfix/bug002` (commit `b81c7f0`)
- Test: `test/test_bug_001.py`
- Resultado: el test pasó correctamente.

---

## Bug 2: Descuento invertido (`1.20` → `0.80`)

### Error

El cupón `SENA2026` debía aplicar un descuento del 20%, pero el código multiplicaba el total por `1.20`.

### Causa

Multiplicar por `1.20` aumenta el precio en un 20%, en lugar de conservar el 80% correspondiente después de descontar el 20%.

### Corrección

Se cambió el factor a `0.80`:

```python
if cupon_descuento == "SENA2026":
    total_pedido = total_pedido * 0.80
```

### Rama y test

- Rama: `bugfix/bug002` (commit `95cf400`)
- Test: `test/test_error2.py`
- Resultado: el test pasó correctamente (tras corregir también el Bug 1).

---

## Bug 3: Producto inexistente en carrito (KeyError)

### Error

En el método `procesar_pedido()`, cuando el carrito contiene un producto cuyo `id_producto` no existe en el inventario, el código accedía directamente a `self.inventario[id_prod]` sin verificar primero si esa clave existe, produciendo un `KeyError` no controlado.

### Corrección

Se agregó una validación de existencia antes del acceso al inventario:

```python
if id_prod not in self.inventario:
    continue
```

Si el producto no existe en el inventario, ese elemento del carrito se ignora y se continúa procesando el resto del pedido.

### Rama y test

- Rama: `bugfix/bug_003`
- Test: `test/test_bug_003.py` (4 tests)
- Resultado: 4 PASSED / 0 FAILED

---

## Bug 4: Stock insuficiente (cantidades negativas)

### Error

El sistema permite procesar una compra aunque la cantidad solicitada sea mayor que el stock disponible. Se descuenta del inventario sin verificar stock suficiente, lo que puede dejar cantidades negativas.

### Corrección

Se agregó una validación antes del descuento:

```python
if cant_comprada > producto['cantidad']:
    continue
```

Si la cantidad solicitada supera el stock disponible, ese item del carrito se ignora y se continúa procesando el resto del pedido.

### Rama y test

- Rama: `bugfix/bug_004`
- Test: `test/test_bug_004.py` (4 tests)
- Resultado: 4 PASSED / 0 FAILED

---

## Bug 5: Iteración insegura en `limpiar_agotados()`

### Error

El método `limpiar_agotados()` iteraba sobre `self.inventario.keys()` mientras eliminaba elementos, causando `RuntimeError: dictionary changed size during iteration`.

### Corrección

Se convirtió la vista de claves en una lista independiente antes de iterar:

```python
for id_producto in list(self.inventario.keys()):
```

### Rama y test

- Rama: `bugfix/bug_005`
- Test: `test/test_bug5.py`
- Resultado: 1 PASSED / 0 FAILED

---

## Bug 6: Argumento mutable por defecto (`inventario_inicial={}`)

### Error

El parámetro `inventario_inicial` utilizaba un diccionario vacío como valor predeterminado:

```python
def __init__(self, inventario_inicial={}):
```

### Causa

Los valores mutables usados como valores predeterminados se crean una sola vez. Por eso, varias instancias de `TiendaOnline` compartían el mismo inventario.

### Corrección

Se cambió el valor predeterminado a `None` y se crea un diccionario nuevo cuando no se recibe un inventario:

```python
def __init__(self, inventario_inicial=None):
    self.inventario = {} if inventario_inicial is None else inventario_inicial
```

### Rama y test

- Rama: `bugfix/bug001` (commit `ce8f763`)
- Test: `test/test_error1.py`
- Resultado: el test pasó correctamente.

---

## Pruebas

Los tests están separados del código de la aplicación dentro de la carpeta `test`.

```text
test/test_bug_001.py      # Bug 1: typo ventas_totaIes
test/test_error2.py       # Bug 2: descuento invertido
test/test_bug_003.py      # Bug 3: producto inexistente
test/test_bug_004.py      # Bug 4: stock insuficiente
test/test_bug5.py         # Bug 5: limpiar_agotados
test/test_error1.py       # Bug 6: inventario compartido
```

Todos los tests pasan correctamente:

```
11 PASSED / 0 FAILED
```

## Commits

```text
ce8f763 fix: corrige inventario compartido (Bug 6)
95cf400 fix: corrige descuento invertido (Bug 2)
b81c7f0 fix: corrige typo ventas_totaIes (Bug 1)
f86b069 fix: soluciona iteración insegura limpiar_agotados (Bug 5)
c9670db fix: corrige stock insuficiente (Bug 4)
0a594dc fix: corrige producto inexistente (Bug 3)
```