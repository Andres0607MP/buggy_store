# Evaluación de Bugs y Pruebas

## Resumen de evaluación

| Fallo                                      | Identificación |  Solución |     Tests |  Subtotal |
| ------------------------------------------ | -------------: | --------: | --------: | --------: |
| Fallo 1 — Argumento mutable por defecto    |            1/1 |       2/2 |       3/3 |   **6/6** |
| Fallo 2 — Typo en variable acumuladora     |            1/1 |       2/2 |       3/3 |   **6/6** |
| Fallo 3 — Cupón que encarecía el pedido    |            1/1 |       2/2 |       3/3 |   **6/6** |
| Fallo 4 — Producto inexistente en carrito  |            1/1 |       2/2 |       3/3 |   **6/6** |
| Fallo 5 — Stock insuficiente               |            1/1 |       2/2 |       3/3 |   **6/6** |
| Fallo 6 — RuntimeError al limpiar agotados |            1/1 |       2/2 |       3/3 |   **6/6** |
| **Total**                                  |        **6/6** | **12/12** | **18/18** | **36/36** |

---

# Fallo 1 — Argumento mutable por defecto

**Bug identificado por el grupo: Bug 6**

### Identificación — 1/1 punto

Explicaron correctamente en el README el problema generado por el uso de un argumento mutable por defecto:

```python
inventario_inicial={}
```

Esto podía provocar que diferentes instancias compartieran el mismo estado en memoria.

### Solución — 2/2 puntos

Cambiaron correctamente el argumento predeterminado a `None` y asignaron un diccionario nuevo cuando no se recibe un inventario inicial.

### Tests — 3/3 puntos

Implementaron `test_inventarios_independientes`, demostrando que modificar el inventario de una tienda no afecta el inventario de una segunda tienda.

### Subtotal

**6/6 puntos**

---

# Fallo 2 — Typo en variable acumuladora

**Bug identificado por el grupo: Bug 1**

### Identificación — 1/1 punto

Encontraron correctamente el error tipográfico en `ventas_totaIes`, donde se utilizaba una `I` mayúscula en lugar de la letra `l`.

Este error provocaba un `AttributeError` al intentar registrar una venta.

### Solución — 2/2 puntos

Renombraron correctamente la variable a:

```python
ventas_totales
```

El cambio fue realizado en la línea 45 de `main.py`.

### Tests — 3/3 puntos

Aunque no adjuntaron el código fuente de la prueba en el fragmento final, documentaron claramente su existencia mediante `test_bug_001.py`.

Además, la salida del runner demuestra que la prueba fue ejecutada correctamente y finalizó de manera exitosa.

### Subtotal

**6/6 puntos**

---

# Fallo 3 — Cupón que encarecía el pedido

**Bug identificado por el grupo: Bug 2**

### Identificación — 1/1 punto

Detectaron correctamente que multiplicar el total por `1.20` aumentaba el precio en un 20 % en lugar de aplicar un descuento.

### Solución — 2/2 puntos

Modificaron correctamente el multiplicador a:

```python
0.80
```

De esta manera, el cupón representa correctamente un descuento del 20 %.

### Tests — 3/3 puntos

Escribieron una prueba clara que verifica que un pedido de **100.000** queda en **80.000** después de aplicar el cupón.

### Subtotal

**6/6 puntos**

---

# Fallo 4 — Producto inexistente en carrito

**Bug identificado por el grupo: Bug 3**

### Identificación — 1/1 punto

Identificaron correctamente que acceder directamente a:

```python
self.inventario[id_prod]
```

sin realizar una validación previa podía provocar un `KeyError` cuando el producto no existiera.

### Solución — 2/2 puntos

Implementaron:

```python
if id_prod not in self.inventario:
    continue
```

Desde el punto de vista técnico, esta implementación evita el colapso del sistema ante un producto inexistente.

A nivel de lógica de negocio, la implementación adopta un modelo de **procesamiento parcial**: los productos inexistentes se ignoran y el sistema continúa procesando los productos válidos del carrito, en lugar de rechazar el carrito completo.

Para los criterios establecidos en esta evaluación, esta solución se considera válida.

### Tests — 3/3 puntos

La suite `test_bug_003.py` presenta una cobertura adecuada del comportamiento.

Las pruebas aíslan los casos mediante workarounds y verifican que los productos inválidos no provoquen modificaciones incorrectas en el inventario.

### Subtotal

**6/6 puntos**

---

# Fallo 5 — Stock insuficiente

**Bug identificado por el grupo: Bug 4**

### Identificación — 1/1 punto

Identificaron correctamente que el sistema permitía descontar una cantidad de unidades superior al stock disponible.

### Solución — 2/2 puntos

Añadieron la validación:

```python
if cant_comprada > producto['cantidad']:
    continue
```

Al igual que en el fallo anterior, la implementación opta por ignorar silenciosamente el producto que excede el stock disponible.

### Tests — 3/3 puntos

Evaluaron de manera exhaustiva diferentes condiciones límite:

* Compra de una cantidad menor al stock.
* Compra de una cantidad igual al stock.
* Compra de una cantidad superior al stock.
* Verificación de que el inventario nunca quede en valores negativos.

### Subtotal

**6/6 puntos**

---

# Fallo 6 — RuntimeError al limpiar agotados

**Bug identificado por el grupo: Bug 5**

### Identificación — 1/1 punto

Comprendieron correctamente que iterar sobre un diccionario y eliminar elementos del mismo diccionario simultáneamente puede provocar una excepción en Python.

### Solución — 2/2 puntos

Forzaron correctamente la creación de una copia de las llaves mediante:

```python
list(self.inventario.keys())
```

Esto permite realizar la iteración sobre una colección independiente mientras se modifica el diccionario original.

### Tests — 3/3 puntos

El test implementado con `unittest` comprueba correctamente que:

* Los productos con stock `0` sean eliminados.
* Los productos que todavía tienen stock permanezcan en el inventario.

### Subtotal

**6/6 puntos**

---

# Resultado de la evaluación

## Puntaje por componente

| Componente     | Puntaje obtenido | Puntaje máximo |
| -------------- | ---------------: | -------------: |
| Identificación |                6 |              6 |
| Solución       |               12 |             12 |
| Tests          |               18 |             18 |
| **Total**      |           **36** |         **36** |

## Puntaje final
Penalización por el orden del repo **-4 puntos**. Tienen un explicacion.md y un README.md en la carpeta de test. Esos archivos no corresponden a esa carpeta. Recuerden que debían refactorizar el código, eso incluye el README.md de la raíz si es que querían hacer las explicaciones de los errores ahí.

**34/36 puntos**
