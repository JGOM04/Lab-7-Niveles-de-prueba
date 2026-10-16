import subprocess
import sys
import unittest


def ejecutar(entradas):
    """Ejecuta main.py como lo haria un usuario real, escribiendo en la consola."""
    resultado = subprocess.run(
        [sys.executable, "main.py"],
        input="\n".join(entradas) + "\n",
        capture_output=True, text=True, timeout=10,
    )
    return resultado.stdout


class TestSistema(unittest.TestCase):
    def test_S01_prestar_libro_desde_menu(self):
        salida = ejecutar(["1", "ISBN001", "U001", "0"])
        self.assertIn("Book successfully borrowed", salida)

    def test_S02_prestar_y_devolver_desde_menu(self):
        salida = ejecutar(["1", "ISBN001", "U001",
                           "2", "ISBN001", "U001",
                           "3", "U001", "0"])
        self.assertIn("Book successfully borrowed", salida)
        self.assertIn("Book successfully returned", salida)

    def test_S03_opcion_invalida(self):
        salida = ejecutar(["9", "0"])
        self.assertIn("Invalid option", salida)

    def test_S04_historial_usuario_inexistente(self):
        salida = ejecutar(["3", "U999", "0"])
        self.assertIn("Error: User not found", salida)

    def test_S05_menu_muestra_libros_disponibles(self):
        salida = ejecutar(["0"])
        self.assertIn("available", salida.lower())


if __name__ == "__main__":
    unittest.main(verbosity=2)