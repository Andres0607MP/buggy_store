### Bug 6: Argumento por defecto mutable (`inventario_inicial={}`)

- **Explicación del error:**
  En la definición del constructor `def __init__(self, inventario_inicial={}):`, el diccionario por defecto `{}` se evalúa una sola vez cuando el intérprete define la clase.

  Por lo tanto, todas las instancias de `TiendaOnline` que se creen sin pasar un argumento explícito compartirán exactamente el mismo objeto diccionario en memoria. Si una tienda agrega un producto, las demás tiendas también podrían tenerlo en su inventario.

- **Solución del error:**
  Se estableció el valor predeterminado del parámetro en `None` y se asigna un nuevo diccionario dentro del cuerpo de `__init__` cuando no se recibe ningún valor.

```python
def __init__(self, inventario_inicial=None):
    if inventario_inicial is None:
        self.inventario = {}
    else:
        self.inventario = inventario_inicial

    self.ventas_totales = 0.0