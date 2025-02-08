from flask import Blueprint, render_template, redirect, url_for, request, jsonify

from api.app.controllers.pagos_controller import ControladorPagos
from api.app.controllers.reservas_controller import ControladorReservas
from api.app.models.users.roles_model import TipoRoles
from api.app.utils.security import Security

pagos_bp = Blueprint('pagos', __name__)

@pagos_bp.route('/servicios/<int:id_servicio>/reservas/<int:id_reserva>/pagos', methods=['POST'])
def efectuar_pago(id_servicio, id_reserva):
    try:
        has_access = Security.verify_token(request.headers)
        if has_access:
            email = has_access.get('email')
            roles = has_access.get('roles')
            if roles and (TipoRoles.CLIENTE.value in roles or TipoRoles.ADMIN.value in roles):
                controller = ControladorPagos()
                return controller.efectuar_pago(id_servicio, id_reserva, email)
        return jsonify({'message': 'Unauthorized'}), 401
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400


# @reservas_bp.route('api/servicios/<int:id_servicio>/reservas/<int:id_reserva>', methods=['PATCH'])
# def actualizar_reservas_por_servicio(id_servicio, id_reserva):
#     has_access = Security.verify_token(request.headers)
#     email= has_access.get('email')
#     roles= has_access.get('roles')
#
#     if has_access and roles and (TipoRoles.PROVEEDOR.value in roles or TipoRoles.ADMIN.value in roles):
#         controller = ControladorReservas()
#         return controller.actualizar_reservas_por_servicio(id_servicio, id_reserva, email)
#
#     else:
#         response = jsonify({'message': 'Unauthorized'})
#         return response, 401
#
@pagos_bp.route('api/pagos', methods=['GET'])
def obtener_pagos():
    has_access = Security.verify_token(request.headers)
    email = has_access.get('email')
    roles= has_access.get('roles')

    if has_access and roles and (TipoRoles.CLIENTE.value in roles or TipoRoles.ADMIN.value in roles):
        controller = ControladorPagos()
        return controller.obtener_pagos(email)

    else:
        response = jsonify({'message': 'Unauthorized'})
        return response, 401

# @reservas_bp.route('api/servicios/<int:id_servicio>/reservas/<int:id_reserva>', methods=['DELETE'])
# def eliminar_reservas_por_servicio(id_servicio, id_reserva):
#     has_access = Security.verify_token(request.headers)
#     email = has_access.get('email')
#     roles = has_access.get('roles')
#
#     if has_access and roles and (TipoRoles.PROVEEDOR.value in roles or TipoRoles.ADMIN.value in roles):
#         controller = ControladorReservas()
#         return controller.eliminar_reservas_por_servicio(id_servicio, id_reserva, email)
#
#     else:
#         response = jsonify({'message': 'Unauthorized'})
#         return response, 401