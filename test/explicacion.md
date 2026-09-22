### Bug 5: Iteración insegura sobre diccionario durante mutación

- **Explicación del error:**
  En el método `limpiar_agotados`, se intentaba eliminar claves de `self.inventario` mientras se iteraba directamente sobre la vista `self.inventario.keys()`. En Python 3, modificar un diccionario mientras se está iterando sobre él provoca una excepción de tipo `RuntimeError: dictionary changed size during iteration`.

- **Solución del error:**
  Se convirtió la vista de claves en una lista independiente usando `list(self.inventario.keys())` antes de realizar la iteración. De esta manera, se puede modificar el diccionario original sin interrumpir el recorrido.

```python
def limpiar_agotados(self):
        """Elimina del inventario los productos con cantidad 0 o menor."""
        for id_producto in list(self.inventario.keys()):
            if self.inventario[id_producto]['cantidad'] <= 0:
                del self.inventario[id_producto]