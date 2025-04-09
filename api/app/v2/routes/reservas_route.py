from flask import request, jsonify
from api.app.models.users.roles_model import TipoRoles
from api.app.utils.responses import APIResponse
from api.app.v2.controllers.reservas_controller import ControladorReservas
from api.app.utils.security import Security, token_required, roles_required

from api.app.v2 import api

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


# @api.route('/servicios/<int:id_servicio>/reservas/<int:id_reserva>', methods=['PATCH'])
# def actualizar_reservas_por_servicio(id_servicio, id_reserva):
#     try:
#         has_access = Security.verify_token(request.headers)
#         if has_access:
#             id_usuario_token = has_access.get('id_usuario')
#             roles = has_access.get('roles')
#             if roles and (TipoRoles.PROVEEDOR.value in roles or TipoRoles.ADMIN.value in roles):
#                 controller = ControladorReservas()
#                 return controller.actualizar_reservas_por_servicio(id_servicio, id_reserva, id_usuario_token, roles)
#         return jsonify({'message': 'Unauthorized'}), 401
#     except Exception as e:
#         return jsonify({'status': 'error', 'message': str(e)}), 400
#
# @api.route('/servicios/<int:id_servicio>/reservas', methods=['GET'])
# def obtener_reservas_por_servicio(id_servicio):
#     try:
#         controller = ControladorReservas()
#         return controller.obtener_reservas_por_servicio(id_servicio)
#     except Exception as e:
#         return jsonify({'status': 'error', 'message': str(e)}), 400
#
# @api.route('/servicios/<int:id_servicio>/reservas/<int:id_reserva>', methods=['DELETE'])
# def eliminar_reservas_por_servicio(id_servicio, id_reserva):
#     try:
#         has_access = Security.verify_token(request.headers)
#         if has_access:
#             id_usuario_token = has_access.get('id_usuario')
#             roles = has_access.get('roles')
#             if roles and (TipoRoles.PROVEEDOR.value in roles or TipoRoles.ADMIN.value in roles):
#                 controller = ControladorReservas()
#                 return controller.eliminar_reservas_por_servicio(id_servicio, id_reserva, id_usuario_token, roles)
#         return jsonify({'message': 'Unauthorized'}), 401
#     except Exception as e:
#         return jsonify({'status': 'error', 'message': str(e)}), 400
