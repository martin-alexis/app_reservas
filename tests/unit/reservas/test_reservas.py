import pytest
from unittest.mock import Mock, patch
from api.app.utils.functions_utils import FunctionsUtils

class TestReservas:
    @patch.object(FunctionsUtils, 'verificar_permisos')
    def test_verificar_permisos_reserva_success(self, mock_verificar_permisos):
        mock_servicio = Mock()
        mock_servicio.id_servicios = 1
        mock_reserva = Mock()
        mock_reserva.servicios_id = 1
        FunctionsUtils.verificar_permisos_reserva(mock_servicio, mock_reserva, 1)
        mock_verificar_permisos.assert_called_once_with(mock_servicio, 1)

    @patch.object(FunctionsUtils, 'verificar_permisos')
    def test_verificar_permisos_reserva_no_pertenece(self, mock_verificar_permisos):
        mock_servicio = Mock()
        mock_servicio.id_servicios = 1
        mock_reserva = Mock()
        mock_reserva.servicios_id = 2
        with pytest.raises(PermissionError, match="La reserva no pertenece"):
            FunctionsUtils.verificar_permisos_reserva(mock_servicio, mock_reserva, 1)

    def test_reserva_pertece_servicio_success(self):
        mock_servicio = Mock()
        mock_servicio.id_servicios = 1
        mock_reserva = Mock()
        mock_reserva.servicios_id = 1
        FunctionsUtils.reserva_pertece_servicio(mock_servicio, mock_reserva)

    def test_reserva_pertece_servicio_no_pertenece(self):
        mock_servicio = Mock()
        mock_servicio.id_servicios = 1
        mock_reserva = Mock()
        mock_reserva.servicios_id = 2
        with pytest.raises(PermissionError, match="La reserva no pertenece"):
            FunctionsUtils.reserva_pertece_servicio(mock_servicio, mock_reserva)

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

    @patch('api.app.utils.functions_utils.EstadosReserva')
    def test_verificar_reserva_ya_reservada_success(self, mock_estados_reserva):
        mock_reserva = Mock()
        mock_reserva.estados_reserva_id = 1
        mock_estado = Mock()
        mock_estado.estado.value = "DISPONIBLE"
        mock_estados_reserva.query.get.return_value = mock_estado
        FunctionsUtils.verificar_reserva_ya_reservada(mock_reserva)

    @patch('api.app.utils.functions_utils.EstadosReserva')
    def test_verificar_reserva_ya_reservada_error(self, mock_estados_reserva):
        mock_reserva = Mock()
        mock_reserva.estados_reserva_id = 1
        mock_estado = Mock()
        mock_estado.estado.value = "RESERVADA"
        mock_estados_reserva.query.get.return_value = mock_estado
        with pytest.raises(PermissionError, match="Esta reserva ya está reservada"):
            FunctionsUtils.verificar_reserva_ya_reservada(mock_reserva)

    @patch('api.app.utils.functions_utils.EstadosReserva')
    def test_poner_reserva_en_estado_reservada_success(self, mock_estados_reserva):
        mock_reserva = Mock()
        mock_estado = Mock()
        mock_estado.id_estados_reserva = 2
        mock_estados_reserva.query.filter_by.return_value.first.return_value = mock_estado
        FunctionsUtils.poner_reserva_en_estado_reservada(mock_reserva)
        assert mock_reserva.estados_reserva_id == 2

    @patch('api.app.utils.functions_utils.EstadosReserva')
    def test_poner_reserva_en_estado_reservada_error(self, mock_estados_reserva):
        mock_reserva = Mock()
        mock_estados_reserva.query.filter_by.return_value.first.return_value = None
        with pytest.raises(ValueError, match="No se encontró el estado RESERVADA"):
            FunctionsUtils.poner_reserva_en_estado_reservada(mock_reserva)

    @patch('api.app.utils.functions_utils.EstadosReserva')
    def test_poner_reserva_en_estado_disponible_success(self, mock_estados_reserva):
        mock_reserva = Mock()
        mock_estado = Mock()
        mock_estado.id_estados_reserva = 1
        mock_estados_reserva.query.filter_by.return_value.first.return_value = mock_estado
        FunctionsUtils.poner_reserva_en_estado_disponible(mock_reserva)
        assert mock_reserva.estados_reserva_id == 1

    @patch('api.app.utils.functions_utils.EstadosReserva')
    def test_poner_reserva_en_estado_disponible_error(self, mock_estados_reserva):
        mock_reserva = Mock()
        mock_estados_reserva.query.filter_by.return_value.first.return_value = None
        with pytest.raises(ValueError, match="No se encontró el estado DISPONIBLE"):
            FunctionsUtils.poner_reserva_en_estado_disponible(mock_reserva)

if __name__ == '__main__':
    pytest.main([__file__, '-v']) 