import json
import unittest
from tests.base_test import BaseTestCase
from api.app.models.users.usuarios_model import Usuarios
from api.app import db

class TestCrearUsuario(BaseTestCase):
    def test_crear_usuario(self):
        """ Prueba de creación de usuario """
        datos_usuario = {
            "nombre": "Pepe",
            "correo": "pepe@gmail.com",
            "contrasena": "123",
            "telefono": "3345679809",
            "tipos_usuario_id": "EMPRESA",
            "roles_id": "PROVEEDOR"
        }

        respuesta = self.client.post(
            "/api/v1.0/usuarios",
            data=json.dumps(datos_usuario),
            content_type="application/json"
        )
        print("Response status:", respuesta.status_code)
        print("Response JSON:", respuesta.get_json())

        self.assertEqual(respuesta.status_code, 201)  # Verificar que se creó correctamente
        json_respuesta = respuesta.get_json()
        self.assertEqual(json_respuesta["status"], "success")

        # Verificar que el usuario se guardó en la base de datos
        with self.app.app_context():
            usuario = Usuarios.query.filter_by(correo="pepe@gmail.com").first()
            self.assertIsNotNone(usuario)
            self.assertEqual(usuario.nombre, "Pepe")


if __name__ == "__main__":
    unittest.main()  # Solo se ejecuta si ejecutas este archivo directamente
