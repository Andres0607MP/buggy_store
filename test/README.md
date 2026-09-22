# Bug 003 y Bug 004 — Documentación de Tests

---

## Bug 003 — Producto inexistente en carrito

### 1. Problema

En el método `procesar_pedido()` de la clase `TiendaOnline` (archivo `main.py`), cuando el carrito contiene un producto cuyo `id_producto` no existe en el inventario, el código accede directamente a `self.inventario[id_prod]` sin verificar primero si esa clave existe.

### 2. Localización

`main.py`, dentro del bucle `for item in carrito:` del método `procesar_pedido()`.

### 3. Excepción

Se produce un `KeyError` no controlado, lo que interrumpe el procesamiento completo del pedido.

### 4. Causa

Falta una guarda condicional que verifique la existencia de `id_prod` en `self.inventario` antes de intentar acceder al diccionario.

### 5. Solución

Se agregó una validación de existencia justo antes del acceso a `self.inventario[id_prod]`:

```python
if id_prod not in self.inventario:
    continue
```

Si el producto no existe en el inventario, ese elemento del carrito se ignora y se continúa procesando el resto del pedido sin interrupciones.

---

## Bug 004 — Stock insuficiente

### 1. Problema

El sistema permite procesar una compra aunque la cantidad solicitada sea mayor que el stock disponible. En el método `procesar_pedido()` de `main.py` se descuenta del inventario sin verificar stock suficiente, lo que puede dejar cantidades negativas.

### 2. Localización

`main.py`, dentro del bucle `for item in carrito:` del método `procesar_pedido()`.

### 3. Causa raíz

No existe una validación previa que compare `cant_comprada` contra `producto['cantidad']` (el stock disponible).

### 4. Comportamiento original

- Cualquier cantidad solicitada se descuenta del stock, incluso si supera lo disponible.
- El stock podía quedar en valores negativos.
- El total se calculaba sobre la cantidad solicitada sin importar el stock real.

### 5. Solución aplicada

Se agregó una validación antes del descuento:

```python
if cant_comprada > producto['cantidad']:
    continue
```

Si la cantidad solicitada supera el stock disponible, ese item del carrito se ignora y se continúa procesando el resto del pedido.

---

## Comportamiento esperado después de ambas soluciones

| Bug | Escenario | Resultado |
|-----|-----------|-----------|
| **Bug 003** | `id_prod` no existe en inventario | Item ignorado, continúa con el resto |
| **Bug 004** | `cant_comprada <= stock` | Se descuenta normalmente y se suma al total |
| **Bug 004** | `cant_comprada == stock` | Stock queda en 0 |
| **Bug 004** | `cant_comprada > stock` | Item ignorado, stock sin cambios, no se suma al total |
| **Bug 004** | Cualquier escenario | Stock nunca es negativo |

---

## Pruebas realizadas

### Bug 003 (`test/test_bug_003.py`)

| Test | Descripción |
|------|-------------|
| `test_bug_003_product_exists_processed_correctly` | Producto existente → procesa correctamente, cantidad y total correctos |
| `test_bug_003_product_not_exists_no_KeyError` | Producto inexistente → no lanza KeyError, total = 0 |
| `test_bug_003_product_not_exists_no_inventory_change` | Producto inexistente → no modifica el inventario |
| `test_bug_003_valid_then_invalid_in_carrito` | Válido + inexistente → válido se procesa, inexistente ignorado |

### Bug 004 (`test/test_bug_004.py`)

| Test | Descripción |
|------|-------------|
| `test_bug_004_compra_dentro_del_stock` | Compra menor al stock → descuento correcto y total calculado |
| `test_bug_004_compra_exactamente_el_stock` | Compra igual al stock → stock termina en 0 |
| `test_bug_004_compra_superior_al_stock` | Compra mayor al stock → item ignorado, stock intacto |
| `test_bug_004_nunca_stock_negativo` | Múltiples compras excesivas → stock nunca negativo |

---

## Comandos de ejecución

```bash
# Bug 003
python -m pytest test/test_bug_003.py -v

# Bug 004
python -m pytest test/test_bug_004.py -v

# Todos los tests
python -m pytest test/ -v
```

---

## Resultados

```
Bug 003: 4 PASSED / 0 FAILED
Bug 004: 4 PASSED / 0 FAILED
```

---

## Aislamiento

Los tests utilizan datos independientes por cada ejecución (`TiendaOnline({})` con un diccionario nuevo) para evitar contaminación entre pruebas. Además, incluyen los ajustes mínimos necesarios para aislar los bugs de **otros bugs presentes en el código original** (como el mutable default en `__init__` y el typo `ventas_totaIes`), sin modificar el código de producción.