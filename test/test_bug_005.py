import sys
import unittest
from pathlib import Path

# Permite importar main.py desde la carpeta superior
sys.path.append(str(Path(__file__).resolve().parent.parent))

from main import TiendaOnline


class TestBug5LimpiarAgotados(unittest.TestCase):

    def test_limpiar_agotados_sin_error(self):
        """
        Bug 5: Verifica que limpiar_agotados no lance RuntimeError
        al iterar y eliminar elementos del inventario.
        """
        tienda = TiendaOnline()
        tienda.agregar_producto("P01", "Teclado Mecánico", 150000, 0)
        tienda.agregar_producto("P02", "Mouse Gamer", 80000, 0)
        tienda.agregar_producto("P03", "Monitor 24'", 600000, 2)

        # Ejecutamos el método
        tienda.limpiar_agotados()

        # Comprobamos los resultados
        self.assertNotIn("P01", tienda.inventario, "P01 debió ser eliminado")
        self.assertNotIn("P02", tienda.inventario, "P02 debió ser eliminado")
        self.assertIn("P03", tienda.inventario, "P03 no debió ser eliminado")
        self.assertEqual(len(tienda.inventario), 1)


if __name__ == "__main__":
    unittest.main()