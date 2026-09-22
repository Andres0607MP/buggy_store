# Bug 004 — Documentación del Test

## Problema

El sistema permite procesar una compra aunque la cantidad solicitada sea mayor que el stock disponible. En el método `procesar_pedido()` de `main.py` se descuenta del inventario sin verificar stock suficiente, lo que puede dejar cantidades negativas.

## Causa raíz

En `main.py`, dentro de `procesar_pedido()`, línea 29:

```python
producto['cantidad'] -= cant_comprada
```

No existe una validación previa que compare `cant_comprada` contra `producto['cantidad']` (el stock disponible).

## Comportamiento original

- Cualquier cantidad solicitada se descuenta del stock, incluso si supera lo disponible.
- El stock podía quedar en valores negativos.
- El total se calculaba sobre la cantidad solicitada sin importar el stock real.

## Solución aplicada

Se agregó una validación antes del descuento:

```python
if cant_comprada > producto['cantidad']:
    continue
```

Si la cantidad solicitada supera el stock disponible, ese item del carrito se ignora y se continúa procesando el resto del pedido.

## Comportamiento esperado después de la solución

| Escenario | Resultado |
|---|---|
| `cant_comprada <= stock` | Se descuenta normalmente y se suma al total |
| `cant_comprada == stock` | Stock queda en 0 |
| `cant_comprada > stock` | Item ignorado, stock sin cambios, no se suma al total |
| Cualquier escenario | Stock nunca es negativo |

## Pruebas realizadas

| Test | Descripción |
|---|---|
| `test_bug_004_compra_dentro_del_stock` | Compra menor al stock → descuento correcto y total calculado |
| `test_bug_004_compra_exactamente_el_stock` | Compra igual al stock → stock termina en 0 |
| `test_bug_004_compra_superior_al_stock` | Compra mayor al stock → item ignorado, stock intacto |
| `test_bug_004_nunca_stock_negativo` | Múltiples compras excesivas → stock nunca negativo |

## Comando de ejecución

```bash
python -m pytest test/test_bug_004.py -v
```

## Resultado

```
4 PASSED / 0 FAILED
```