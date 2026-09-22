# Buggy Store

## Contexto

Acabamos de heredar el backend de una pequeña tienda en línea escrito por un desarrollador junior. El sistema permite registrar productos, procesar compras y limpiar el inventario, pero contiene varios errores.

Este trabajo documenta y corrige únicamente los Bugs 1 y 2.

## Bug 1: Datos compartidos

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

- Rama: `bugfix/error1`
- Test: `test/test_error1.py`
- Resultado: el test pasó correctamente.

## Bug 2: Descuento invertido

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

- Rama: `bugfix/error2`
- Test: `test/test_error2.py`
- Resultado: el test alcanza la lógica del descuento, pero queda bloqueado por otro bug preexistente en `ventas_totaIes`, que no pertenece a los Bugs 1 y 2.

## Pruebas

Los tests están separados del código de la aplicación dentro de la carpeta `test`.

```text
test/test_error1.py
test/test_error2.py
```

Pytest no está instalado en el entorno actual. El test del Bug 1 fue ejecutado directamente y pasó. El test del Bug 2 fue ejecutado directamente y reveló el error independiente de `ventas_totaIes`.

## Commits

```text
ce8f763 fix: corrige inventario compartido
95cf400 fix: corrige descuento invertido
```