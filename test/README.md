# Bug 001–006 — Documentación de Tests

---

## Bug 1 — Typo en atributo de ventas (`ventas_totaIes` → `ventas_totales`)

### Problema

En el método `procesar_pedido()`, al registrar la venta, se usaba un atributo con typo:

```python
self.ventas_totaIes += total_pedido
```

El atributo correcto es `ventas_totales` (declarado en `__init__`), por lo que el código lanzaba `AttributeError`.

### Solución

Se corrigió el nombre:

```python
self.ventas_totales += total_pedido
```

### Test

`test/test_bug_001.py` — Verifica que `procesar_pedido()` no lance `AttributeError` y que `ventas_totales` se actualice.

### Resultado

```
1 PASSED / 0 FAILED
```

---

## Bug 2 — Descuento invertido (`1.20` → `0.80`)

### Problema

El cupón `SENA2026` multiplicaba el total por `1.20` (aumenta 20%) en lugar de `0.80` (descuenta 20%).

### Solución

```python
if cupon_descuento == "SENA2026":
    total_pedido = total_pedido * 0.80
```

### Test

`test/test_error2.py` — Verifica que el total con cupón sea 80% del original.

### Resultado

```
1 PASSED / 0 FAILED
```

---

## Bug 3 — Producto inexistente en carrito (KeyError)

### Problema

En `procesar_pedido()`, se accedía a `self.inventario[id_prod]` sin verificar existencia, produciendo `KeyError`.

### Solución

```python
if id_prod not in self.inventario:
    continue
```

### Tests (`test/test_bug_003.py`)

| Test | Descripción |
|------|-------------|
| `test_bug_003_product_exists_processed_correctly` | Producto existente → procesa correctamente |
| `test_bug_003_product_not_exists_no_KeyError` | Inexistente → no lanza KeyError |
| `test_bug_003_product_not_exists_no_inventory_change` | Inexistente → no modifica inventario |
| `test_bug_003_valid_then_invalid_in_carrito` | Válido + inexistente → válido procesa, inexistente ignorado |

### Resultado

```
4 PASSED / 0 FAILED
```

---

## Bug 4 — Stock insuficiente (cantidades negativas)

### Problema

Se descontaba stock sin verificar disponibilidad, permitiendo cantidades negativas.

### Solución

```python
if cant_comprada > producto['cantidad']:
    continue
```

### Tests (`test/test_bug_004.py`)

| Test | Descripción |
|------|-------------|
| `test_bug_004_compra_dentro_del_stock` | Compra ≤ stock → descuenta correctamente |
| `test_bug_004_compra_exactamente_el_stock` | Compra == stock → stock = 0 |
| `test_bug_004_compra_superior_al_stock` | Compra > stock → item ignorado |
| `test_bug_004_nunca_stock_negativo` | Múltiples excesos → stock nunca negativo |

### Resultado

```
4 PASSED / 0 FAILED
```

---

## Bug 5 — Iteración insegura en `limpiar_agotados()`

### Problema

`limpiar_agotados()` iteraba sobre `self.inventario.keys()` mientras eliminaba claves, causando `RuntimeError`.

### Solución

```python
for id_producto in list(self.inventario.keys()):
```

### Test

`test/test_bug5.py` — Verifica que productos con stock 0 se eliminen y los demás se conserven sin `RuntimeError`.

### Resultado

```
1 PASSED / 0 FAILED
```

---

## Bug 6 — Argumento mutable por defecto (`inventario_inicial={}`)

### Problema

El constructor usaba `inventario_inicial={}`, causando que todas las instancias compartieran el mismo dict.

### Solución

```python
def __init__(self, inventario_inicial=None):
    self.inventario = {} if inventario_inicial is None else inventario_inicial
```

### Test

`test/test_error1.py` — Verifica que dos instancias tengan inventarios independientes.

### Resultado

```
1 PASSED / 0 FAILED
```

---

## Resumen de ejecución

```bash
python -m pytest test/ -v
```

```
test/test_bug_001.py      PASSED
test/test_error2.py       PASSED
test/test_bug_003.py      4 PASSED
test/test_bug_004.py      4 PASSED
test/test_bug5.py         PASSED
test/test_error1.py       PASSED
===========================
11 PASSED / 0 FAILED
```