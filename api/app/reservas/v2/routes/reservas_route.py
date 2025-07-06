from flask import request
from api.app.usuarios.models.roles_model import TipoRoles
from api.app.utils.responses import APIResponse
from api.app.reservas.v2.controllers.reservas_controller import ControladorReservas
from api.app.utils.security import token_required, roles_required
from api.app.utils import common_routes as common


from api.app.blueprints_v2 import api

@api.route('/reservas/<int:id_reserva>', methods=['GET'])
def obtener_reserva_por__id (id_reserva):
       return common.obtener_reserva_por_id(id_reserva)

@api.route('/servicios/<int:id_servicio>/reservas', methods=['POST'])
@token_required
@roles_required([TipoRoles.PROVEEDOR.value, TipoRoles.ADMIN.value])
def crear_reservas(payload, id_servicio):
    try:
        id_usuario_token = payload.get('id_usuario')
        data = request.json
        controller = ControladorReservas()
        return controller.crear_reservas(data, id_usuario_token, id_servicio)
    except Exception as e:
        return APIResponse.error(message=str(e))

@api.route('/servicios/<int:id_servicio>/reservas/<int:id_reserva>', methods=['PATCH'])
@token_required
@roles_required([TipoRoles.PROVEEDOR.value, TipoRoles.ADMIN.value])
def actualizar_reservas(payload, id_servicio, id_reserva):
    try:
        id_usuario_token = payload.get('id_usuario')
        data = request.json
        controller = ControladorReservas()
        return controller.actualizar_reservas(data, id_usuario_token, id_servicio, id_reserva)
    except Exception as e:
        return APIResponse.error(message=str(e))

@api.route('/servicios/<int:id_servicio>/reservas/<int:id_reserva>', methods=['DELETE'])
@token_required
@roles_required([TipoRoles.PROVEEDOR.value, TipoRoles.ADMIN.value])
def eliminar_reservas(payload, id_servicio, id_reserva):
    try:
        id_usuario_token = payload.get('id_usuario')
        controller = ControladorReservas()
        return controller.eliminar_reservas( id_usuario_token, id_servicio, id_reserva)
    except Exception as e:
        return APIResponse.error(message=str(e))

