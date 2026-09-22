import sys
import unittest
from pathlib import Path

# Permite importar main.py desde la carpeta superior
sys.path.append(str(Path(__file__).resolve().parent.parent))

from main import TiendaOnline


class TestBug6InventarioCompartido(unittest.TestCase):

    def test_inventarios_son_independientes(self):
        """
        Bug 6: Verifica que dos instancias creadas sin argumentos
        tengan inventarios totalmente independientes en memoria.
        """
        tienda1 = TiendaOnline()
        tienda2 = TiendaOnline()

        # Agregamos un producto únicamente a la tienda 1
        tienda1.agregar_producto("P01", "Teclado Mecánico", 150000, 5)

        # Verificaciones
        self.assertIn("P01", tienda1.inventario, "La tienda 1 debe contener el producto")
        self.assertNotIn("P01", tienda2.inventario, "La tienda 2 NO debe compartir el inventario de la tienda 1")
        self.assertEqual(len(tienda2.inventario), 0, "El inventario de la tienda 2 debe estar vacío")


if __name__ == "__main__":
    unittest.main()