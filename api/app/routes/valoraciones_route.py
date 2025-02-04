from flask import Blueprint, render_template, redirect, url_for, request, jsonify

from api.app.controllers.reservas_controller import ControladorReservas
from api.app.models.users.roles_model import TipoRoles
from api.app.utils.security import Security

valoraciones_bp = Blueprint('valoraciones', __name__)

@valoraciones_bp.route('/api/servicios/<int:id_servicio>/valoraciones', methods=['POST'])
def crear_valoraciones(id_servicio):
    has_access = Security.verify_token(request.headers)
    roles = has_access.get('roles')

    if has_access and roles and (TipoRoles.PROVEEDOR.value in roles or TipoRoles.ADMIN.value in roles):
        controller = ControladorReservas()
        return controller.crear_reservas(id_servicio)

    else:
        response = jsonify({'message': 'Unauthorized'})
        return response, 401

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
# @reservas_bp.route('api/servicios/<int:id_servicio>/reservas', methods=['GET'])
# def obtener_reservas_por_servicio(id_servicio):
#     has_access = Security.verify_token(request.headers)
#     email = has_access.get('email')
#     roles= has_access.get('roles')
#
#     if has_access and roles and (TipoRoles.PROVEEDOR.value in roles or TipoRoles.ADMIN.value in roles):
#         controller = ControladorReservas()
#         return controller.obtener_reservas_por_servicio(email, id_servicio)
#
#     else:
#         response = jsonify({'message': 'Unauthorized'})
#         return response, 401
#
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