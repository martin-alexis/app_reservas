# tests/base_test.py
import unittest
from your_app import app, db

class BaseTestCase(unittest.TestCase):
    def setUp(self):
        """ Se ejecuta antes de cada prueba """
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()  # Crea las tablas en la base de datos en memoria

    def tearDown(self):
        """ Se ejecuta después de cada prueba """
        db.session.remove()
        db.drop_all()  # Borra todas las tablas
        self.app_context.pop()
