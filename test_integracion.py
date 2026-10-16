import unittest
import library
from library import Library
from book import Book
from user import User


class TestIntegracion(unittest.TestCase):
    def setUp(self):
        library.settings["loans_enabled"] = True
        self.lib = Library()
        self.libro = Book("1984", "George Orwell", 1949, "ISBN001")
        self.anna = User("Anna", "U001")
        self.juan = User("Juan", "U002")
        self.lib.add_book(self.libro)
        self.lib.add_user(self.anna)
        self.lib.add_user(self.juan)

    def test_I01_agregar_libro_y_usuario_y_prestar(self):
        self.lib.borrow_book("U001", "ISBN001")
        self.assertTrue(self.libro.borrowed)
        self.assertEqual(len(self.anna.get_history()), 1)

    def test_I02_rechazo_de_libro_ya_prestado(self):
        self.lib.borrow_book("U001", "ISBN001")
        with self.assertRaises(ValueError):
            self.lib.borrow_book("U002", "ISBN001")
        self.assertEqual(self.juan.get_history(), [])

    def test_I03_devolver_y_prestar_a_otro_usuario(self):
        self.lib.borrow_book("U001", "ISBN001")
        self.lib.return_book("U001", "ISBN001")
        self.lib.borrow_book("U002", "ISBN001")
        self.assertTrue(self.libro.borrowed)
        self.assertEqual(len(self.anna.get_history()), 2)
        self.assertEqual(len(self.juan.get_history()), 1)

    def test_I04_prestamos_deshabilitados(self):
        library.settings["loans_enabled"] = False
        self.lib.borrow_book("U001", "ISBN001")
        self.assertFalse(self.libro.borrowed)
        library.settings["loans_enabled"] = True


if __name__ == "__main__":
    unittest.main(verbosity=2)