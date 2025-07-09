import pytest
from unittest.mock import Mock, patch
from api.app.utils.functions_utils import FunctionsUtils

class TestGenerales:
    def test_pasar_ids_success(self):
        data = {'tipo_roles': None}
        ids = [1, 2, 3]
        result = FunctionsUtils.pasar_ids(data, 'tipo_roles', ids)
        assert result['tipo_roles'] == [1, 2, 3]

    def test_pasar_ids_empty_list(self):
        data = {'tipo_roles': None}
        ids = []
        result = FunctionsUtils.pasar_ids(data, 'tipo_roles', ids)
        assert result['tipo_roles'] == []

    def test_pasar_ids_single_object(self):
        data = {'tipos_usuario': None}
        ids = [1]
        result = FunctionsUtils.pasar_ids(data, 'tipos_usuario', ids)
        assert result['tipos_usuario'] == 1

    def test_pasar_ids_different_attribute(self):
        data = {'id_servicios': None}
        ids = [10, 20]
        result = FunctionsUtils.pasar_ids(data, 'id_servicios', ids)
        assert result['id_servicios'] == 10

    def test_pasar_ids_campo_no_existe(self):
        data = {'otro_campo': 'valor'}
        ids = [1, 2, 3]
        result = FunctionsUtils.pasar_ids(data, 'tipo_roles', ids)
        assert 'tipo_roles' not in result
        assert result['otro_campo'] == 'valor'

    @patch.object(FunctionsUtils, 'get_roles_user')
    def test_verificar_permisos_unknown_object(self, mock_get_roles):
        mock_unknown = Mock()
        mock_get_roles.return_value = ['CLIENTE']
        with pytest.raises(ValueError, match="Tipo de objeto no soportado"):
            FunctionsUtils.verificar_permisos(mock_unknown, 1)

if __name__ == '__main__':
    pytest.main([__file__, '-v']) 