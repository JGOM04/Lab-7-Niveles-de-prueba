import unittest
from io import StringIO
from unittest.mock import patch
from book import Book
from user import User
from library import Library


class TestBook(unittest.TestCase):
    def setUp(self):
        self.book = Book("1984", "George Orwell", 1949, "ISBN001")

    def test_U01_libro_nuevo_esta_disponible(self):
        self.assertFalse(self.book.borrowed)

    def test_U02_prestar_libro_disponible(self):
        self.book.borrow()
        self.assertTrue(self.book.borrowed)

    def test_U03_prestar_libro_ya_prestado(self):
        self.book.borrow()
        with self.assertRaises(ValueError):
            self.book.borrow()

    def test_U04_devolver_libro_no_prestado(self):
        with self.assertRaises(ValueError):
            self.book.return_book()


class TestUser(unittest.TestCase):
    def setUp(self):
        self.user = User("Anna", "U001")
        self.book = Book("1984", "George Orwell", 1949, "ISBN001")

    def test_U05_historial_registra_prestamo(self):
        self.user.register_borrow(self.book)
        self.assertEqual(self.user.get_history(), ["Borrowed: 1984"])

    def test_U06_historial_registra_devolucion(self):
        self.user.register_return(self.book)
        self.assertEqual(self.user.get_history(), ["Returned: 1984"])


class TestLibrary(unittest.TestCase):
    def setUp(self):
        self.lib = Library()
        self.lib.add_user(User("Anna", "U001"))
        self.lib.add_book(Book("1984", "George Orwell", 1949, "ISBN001"))

    def test_U07_buscar_usuario_inexistente(self):
        with self.assertRaises(ValueError):
            self.lib._find_user("U999")

    def test_U08_buscar_usuario_existente_sin_mensaje_error(self):
        with patch("sys.stdout", new_callable=StringIO) as salida:
            user = self.lib._find_user("U001")
        self.assertEqual(user.name, "Anna")
        self.assertNotIn("User not found", salida.getvalue())

    def test_U09_buscar_libro_inexistente(self):
        with self.assertRaises(ValueError):
            self.lib._find_book("ISBN999")


if __name__ == "__main__":
    unittest.main(verbosity=2)