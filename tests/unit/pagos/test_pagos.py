import pytest
from unittest.mock import Mock, patch
from api.app.utils.functions_utils import FunctionsUtils

class TestPagos:
    @patch.object(FunctionsUtils, 'get_roles_user')
    def test_verificar_permisos_eliminar_pago_duenio(self, mock_get_roles):
        mock_pago = Mock()
        mock_pago.usuarios_id = 1
        FunctionsUtils.verificar_permisos_eliminar_pago(mock_pago, 1)

    @patch.object(FunctionsUtils, 'get_roles_user')
    def test_verificar_permisos_eliminar_pago_admin(self, mock_get_roles):
        mock_pago = Mock()
        mock_pago.usuarios_id = 2
        mock_get_roles.return_value = ['ADMIN']
        FunctionsUtils.verificar_permisos_eliminar_pago(mock_pago, 1)

    @patch.object(FunctionsUtils, 'get_roles_user')
    def test_verificar_permisos_eliminar_pago_no_permission(self, mock_get_roles):
        mock_pago = Mock()
        mock_pago.usuarios_id = 2
        mock_get_roles.return_value = ['CLIENTE']
        with pytest.raises(PermissionError, match="No tienes permisos"):
            FunctionsUtils.verificar_permisos_eliminar_pago(mock_pago, 1)

    def test_verificar_pago_monto_exactitud_success(self):
        mock_servicio = Mock()
        mock_servicio.precio = 100.0
        FunctionsUtils.verificar_pago_monto_exactitud(mock_servicio, 100.0)

    def test_verificar_pago_monto_exactitud_error(self):
        mock_servicio = Mock()
        mock_servicio.precio = 100.0
        with pytest.raises(ValueError, match="El pago del servicio tiene que ser exacto"):
            FunctionsUtils.verificar_pago_monto_exactitud(mock_servicio, 90.0)

    def test_verificar_pago_monto_exactitud_float_precision(self):
        mock_servicio = Mock()
        mock_servicio.precio = 99.99
        FunctionsUtils.verificar_pago_monto_exactitud(mock_servicio, 99.99)

    def test_verificar_pago_monto_exactitud_zero_price(self):
        mock_servicio = Mock()
        mock_servicio.precio = 0.0
        FunctionsUtils.verificar_pago_monto_exactitud(mock_servicio, 0.0)

    def test_verificar_pago_pertenece_reserva_servicio_success(self):
        mock_servicio = Mock()
        mock_servicio.id_servicios = 1
        mock_reserva = Mock()
        mock_reserva.servicios_id = 1
        mock_reserva.id_reservas = 1
        mock_pago = Mock()
        mock_pago.reservas_id = 1
        FunctionsUtils.verificar_pago_pertenece_reserva_servicio(mock_servicio, mock_reserva, mock_pago)

    def test_verificar_pago_pertenece_reserva_servicio_reserva_error(self):
        mock_servicio = Mock()
        mock_servicio.id_servicios = 1
        mock_reserva = Mock()
        mock_reserva.servicios_id = 2
        mock_pago = Mock()
        with pytest.raises(PermissionError, match="La reserva no pertenece"):
            FunctionsUtils.verificar_pago_pertenece_reserva_servicio(mock_servicio, mock_reserva, mock_pago)

    def test_verificar_pago_pertenece_reserva_servicio_pago_error(self):
        mock_servicio = Mock()
        mock_servicio.id_servicios = 1
        mock_reserva = Mock()
        mock_reserva.servicios_id = 1
        mock_reserva.id_reservas = 1
        mock_pago = Mock()
        mock_pago.reservas_id = 2
        with pytest.raises(PermissionError, match="El pago no pertenece"):
            FunctionsUtils.verificar_pago_pertenece_reserva_servicio(mock_servicio, mock_reserva, mock_pago)

if __name__ == '__main__':
    pytest.main([__file__, '-v']) 