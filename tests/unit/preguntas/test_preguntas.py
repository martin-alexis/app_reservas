import pytest
from unittest.mock import Mock, patch
from api.app.utils.functions_utils import FunctionsUtils

class TestPreguntas:
    @patch.object(FunctionsUtils, 'get_roles_user')
    def test_verificar_usuario_pregunta_proveedor_admin(self, mock_get_roles):
        mock_servicio = Mock()
        mock_servicio.usuarios_proveedores_id = 1
        mock_get_roles.return_value = ['ADMIN']
        FunctionsUtils.verificar_usuario_pregunta(mock_servicio, 1)

    @patch.object(FunctionsUtils, 'get_roles_user')
    def test_verificar_usuario_pregunta_proveedor_no_admin(self, mock_get_roles):
        mock_servicio = Mock()
        mock_servicio.usuarios_proveedores_id = 1
        mock_get_roles.return_value = ['CLIENTE']
        with pytest.raises(PermissionError, match="Los dueños del servicio no pueden preguntar"):
            FunctionsUtils.verificar_usuario_pregunta(mock_servicio, 1)

    def test_verificar_usuario_pregunta_no_proveedor(self):
        mock_servicio = Mock()
        mock_servicio.usuarios_proveedores_id = 2
        FunctionsUtils.verificar_usuario_pregunta(mock_servicio, 1)

    def test_pregunta_pertenece_servicio_success(self):
        mock_servicio = Mock()
        mock_servicio.id_servicios = 1
        mock_pregunta = Mock()
        mock_pregunta.servicios_id = 1
        FunctionsUtils.pregunta_pertenece_servicio(mock_servicio, mock_pregunta)

    def test_pregunta_pertenece_servicio_no_pertenece(self):
        mock_servicio = Mock()
        mock_servicio.id_servicios = 1
        mock_pregunta = Mock()
        mock_pregunta.servicios_id = 2
        with pytest.raises(PermissionError, match="La pregunta no pertenece"):
            FunctionsUtils.pregunta_pertenece_servicio(mock_servicio, mock_pregunta)

    def test_verificar_permisos_eliminar_pregunta_proveedor(self):
        mock_servicio = Mock()
        mock_servicio.usuarios_proveedores_id = 1
        mock_pregunta = Mock()
        mock_pregunta.usuarios_pregunta_id = 2
        FunctionsUtils.verificar_permisos_eliminar_pregunta(mock_servicio, mock_pregunta, 1)

    def test_verificar_permisos_eliminar_pregunta_autor(self):
        mock_servicio = Mock()
        mock_servicio.usuarios_proveedores_id = 2
        mock_pregunta = Mock()
        mock_pregunta.usuarios_pregunta_id = 1
        FunctionsUtils.verificar_permisos_eliminar_pregunta(mock_servicio, mock_pregunta, 1)

    def test_verificar_permisos_eliminar_pregunta_no_permission(self):
        mock_servicio = Mock()
        mock_servicio.usuarios_proveedores_id = 2
        mock_pregunta = Mock()
        mock_pregunta.usuarios_pregunta_id = 3
        with pytest.raises(PermissionError, match="No tienes permisos"):
            FunctionsUtils.verificar_permisos_eliminar_pregunta(mock_servicio, mock_pregunta, 1)

    def test_verificar_permisos_eliminar_pregunta_proveedor_autor_same_user(self):
        mock_servicio = Mock()
        mock_servicio.usuarios_proveedores_id = 1
        mock_pregunta = Mock()
        mock_pregunta.usuarios_pregunta_id = 1
        FunctionsUtils.verificar_permisos_eliminar_pregunta(mock_servicio, mock_pregunta, 1)

if __name__ == '__main__':
    pytest.main([__file__, '-v']) 