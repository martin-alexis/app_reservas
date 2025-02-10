from flask import Blueprint, request, jsonify
from api.app.models.users.roles_model import TipoRoles
from api.app.controllers.reservas_controller import ControladorReservas
from api.app.utils.security import Security

reservas_bp = Blueprint('reservas', __name__)

@reservas_bp.route('/api/v1.0/servicios/<int:id_servicio>/reservas', methods=['POST'])
def crear_reservas(id_servicio):
    try:
        has_access = Security.verify_token(request.headers)
        if has_access:
            roles = has_access.get('roles')
            if roles and (TipoRoles.PROVEEDOR.value in roles or TipoRoles.ADMIN.value in roles):
                controller = ControladorReservas()
                return controller.crear_reservas(id_servicio)
        return jsonify({'message': 'Unauthorized'}), 401
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

@reservas_bp.route('/api/v1.0/servicios/<int:id_servicio>/reservas/<int:id_reserva>', methods=['PUT'])
def actualizar_reservas_por_servicio(id_servicio, id_reserva):
    try:
        has_access = Security.verify_token(request.headers)
        if has_access:
            email = has_access.get('email')
            roles = has_access.get('roles')
            if roles and (TipoRoles.PROVEEDOR.value in roles or TipoRoles.ADMIN.value in roles):
                controller = ControladorReservas()
                return controller.actualizar_reservas_por_servicio(id_servicio, id_reserva, email)
        return jsonify({'message': 'Unauthorized'}), 401
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

@reservas_bp.route('/api/v1.0/servicios/<int:id_servicio>/reservas', methods=['GET'])
def obtener_reservas_por_servicio(id_servicio):
    try:
        has_access = Security.verify_token(request.headers)
        if has_access:
            email = has_access.get('email')
            roles = has_access.get('roles')
            if roles and (TipoRoles.PROVEEDOR.value in roles or TipoRoles.ADMIN.value in roles):
                controller = ControladorReservas()
                return controller.obtener_reservas_por_servicio(email, id_servicio)
        return jsonify({'message': 'Unauthorized'}), 401
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

@reservas_bp.route('/api/v1.0/servicios/<int:id_servicio>/reservas/<int:id_reserva>', methods=['DELETE'])
def eliminar_reservas_por_servicio(id_servicio, id_reserva):
    try:
        has_access = Security.verify_token(request.headers)
        if has_access:
            email = has_access.get('email')
            roles = has_access.get('roles')
            if roles and (TipoRoles.PROVEEDOR.value in roles or TipoRoles.ADMIN.value in roles):
                controller = ControladorReservas()
                return controller.eliminar_reservas_por_servicio(id_servicio, id_reserva, email)
        return jsonify({'message': 'Unauthorized'}), 401
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400
