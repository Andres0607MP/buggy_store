# Bug 003 — Documentación del Test

## 1. Bug 003

**Problema:** En el método `procesar_pedido()` de la clase `TiendaOnline` (archivo `main.py`), cuando el carrito contiene un producto cuyo `id_producto` no existe en el inventario, el código accede directamente a `self.inventario[id_prod]` sin verificar primero si esa clave existe.

**Localización:** `main.py`, dentro del bucle `for item in carrito:` del método `procesar_pedido()`, en la línea:

```python
producto = self.inventario[id_prod]
```

**Excepción:** Se produce un `KeyError` no controlado, lo que interrumpe el procesamiento completo del pedido.

**Causa:** Falta una guarda condicional que verifique la existencia de `id_prod` en `self.inventario` antes de intentar acceder al diccionario. El método asume que todo producto del carrito existe en el inventario, lo cual no siempre es cierto.

---

## 2. Solución

Se agregó una validación de existencia justo antes del acceso a `self.inventario[id_prod]`:

```python
if id_prod not in self.inventario:
    continue
```

Si el producto no existe en el inventario, ese elemento del carrito se ignora y se continúa procesando el resto del pedido sin interrupciones. Los productos válidos que aparezcan después sí se procesan normalmente.

Esta corrección es mínima: no altera ninguna otra parte de la lógica del método ni del sistema.

---

## 3. Pruebas

El archivo `test/test_bug_003.py` contiene 4 pruebas unitarias que validan el comportamiento corregido:

| Test | Descripción |
|---|---|
| `test_bug_003_product_exists_processed_correctly` | Un producto existente en el inventario se procesa correctamente: se descuenta la cantidad y se calcula el total. |
| `test_bug_003_product_not_exists_no_KeyError` | Un producto inexistente **no lanza `KeyError`**. El método retorna el total sin cambios. |
| `test_bug_003_product_not_exists_no_inventory_change` | Un producto inexistente **no modifica ni agrega nada** al inventario. |
| `test_bug_003_valid_then_invalid_in_carrito` | Si el carrito contiene un producto válido seguido de uno inexistente, el válido se procesa y el inexistente se ignora. |

---

## 4. Ejecución

Para ejecutar los tests de Bug 003:

```bash
python -m pytest test/test_bug_003.py -v
```

---

## 5. Resultado

Actualmente los 4 tests pasan correctamente:

```
4 PASSED / 0 FAILED
```

---

## 6. Aislamiento

Los tests utilizan datos independientes por cada ejecución (`TiendaOnline({})` con un diccionario nuevo) para evitar contaminación entre pruebas. Además, incluyen los ajustes mínimos necesarios para aislar Bug 003 de **otros bugs presentes en el código original** (como el mutable default en `__init__` y el typo `ventas_totaIes` en la línea 40), sin modificar el código de producción.

Ninguno de estos ajustes corrige los otros bugs; únicamente permiten que el test se ejecute y valide exclusivamente el comportamiento esperado del Bug 003.