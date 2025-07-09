import pytest
from unittest.mock import Mock, patch
from api.app.utils.functions_utils import FunctionsUtils

class TestUsuarios:
    @patch('api.app.utils.functions_utils.UsuariosTieneRoles')
    @patch('api.app.utils.functions_utils.Roles')
    def test_get_roles_user_success(self, mock_roles, mock_user_roles):
        rel1 = Mock(roles_id=1)
        rel2 = Mock(roles_id=2)
        role1 = Mock(tipo="TipoRoles.ADMIN")
        role2 = Mock(tipo="TipoRoles.CLIENTE")
        mock_user_roles.query.filter_by.return_value.all.return_value = [rel1, rel2]
        mock_roles.query.get.side_effect = lambda x: role1 if x == 1 else role2
        result = FunctionsUtils.get_roles_user(1)
        assert result == ["ADMIN", "CLIENTE"]
        mock_user_roles.query.filter_by.assert_called_once_with(usuarios_id=1)

    @patch('api.app.utils.functions_utils.UsuariosTieneRoles')
    def test_get_roles_user_no_roles(self, mock_user_roles):
        mock_user_roles.query.filter_by.return_value.all.return_value = []
        result = FunctionsUtils.get_roles_user(1)
        assert result == []
        mock_user_roles.query.filter_by.assert_called_once_with(usuarios_id=1)

    @patch('api.app.utils.functions_utils.UsuariosTieneRoles')
    @patch('api.app.utils.functions_utils.Roles')
    def test_get_roles_user_role_not_found(self, mock_roles, mock_user_roles):
        rel = Mock(roles_id=999)
        mock_user_roles.query.filter_by.return_value.all.return_value = [rel]
        mock_roles.query.get.return_value = None
        result = FunctionsUtils.get_roles_user(1)
        assert result == []
        mock_roles.query.get.assert_called_once_with(999)

    @patch('api.app.utils.functions_utils.Usuarios')
    def test_obtener_usuario_por_correo_success(self, mock_usuarios):
        mock_usuario = Mock()
        mock_usuario.id_usuarios = 1
        mock_usuario.nombre = "Juan Pérez"
        mock_usuario.correo = "juan@example.com"
        mock_usuarios.query.filter_by.return_value.first.return_value = mock_usuario
        result = FunctionsUtils.obtener_usuario_por_correo("juan@example.com")
        assert result == mock_usuario
        assert result.id_usuarios == 1
        assert result.nombre == "Juan Pérez"
        mock_usuarios.query.filter_by.assert_called_once_with(correo="juan@example.com")

    @patch('api.app.utils.functions_utils.Usuarios')
    def test_obtener_usuario_por_correo_not_found(self, mock_usuarios):
        mock_usuarios.query.filter_by.return_value.first.return_value = None
        result = FunctionsUtils.obtener_usuario_por_correo("inexistente@example.com")
        assert result is None
        mock_usuarios.query.filter_by.assert_called_once_with(correo="inexistente@example.com")

    @patch('api.app.utils.functions_utils.Usuarios')
    def test_obtener_usuario_por_correo_empty_string(self, mock_usuarios):
        mock_usuarios.query.filter_by.return_value.first.return_value = None
        result = FunctionsUtils.obtener_usuario_por_correo("")
        assert result is None
        mock_usuarios.query.filter_by.assert_called_once_with(correo="")

    @patch('api.app.utils.functions_utils.Usuarios')
    def test_obtener_usuario_por_correo_none_input(self, mock_usuarios):
        mock_usuarios.query.filter_by.return_value.first.return_value = None
        result = FunctionsUtils.obtener_usuario_por_correo(None)
        assert result is None
        mock_usuarios.query.filter_by.assert_called_once_with(correo=None)

if __name__ == '__main__':
    pytest.main([__file__, '-v']) 