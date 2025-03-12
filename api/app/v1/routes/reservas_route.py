from flask import Blueprint, request, jsonify
from api.app.models.users.roles_model import TipoRoles
from api.app.v1.controllers.reservas_controller import ControladorReservas
from api.app.utils.security import Security

reservas_bp = Blueprint('reservas', __name__)

@reservas_bp.route('/api/v1.0/servicios/<int:id_servicio>/reservas', methods=['POST'])
def crear_reservas(id_servicio):
    try:
        has_access = Security.verify_token(request.headers)
        if has_access:
            roles = has_access.get('roles')
            id_usuario_token = has_access.get('id_usuario')
            if roles and (TipoRoles.PROVEEDOR.value in roles or TipoRoles.ADMIN.value in roles):
                controller = ControladorReservas()
                return controller.crear_reservas(id_servicio, id_usuario_token, roles)
        return jsonify({'message': 'Unauthorized'}), 401
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

@reservas_bp.route('/api/v1.0/servicios/<int:id_servicio>/reservas/<int:id_reserva>', methods=['PATCH'])
def actualizar_reservas_por_servicio(id_servicio, id_reserva):
    try:
        has_access = Security.verify_token(request.headers)
        if has_access:
            id_usuario_token = has_access.get('id_usuario')
            roles = has_access.get('roles')
            if roles and (TipoRoles.PROVEEDOR.value in roles or TipoRoles.ADMIN.value in roles):
                controller = ControladorReservas()
                return controller.actualizar_reservas_por_servicio(id_servicio, id_reserva, id_usuario_token, roles)
        return jsonify({'message': 'Unauthorized'}), 401
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

@reservas_bp.route('/api/v1.0/servicios/<int:id_servicio>/reservas', methods=['GET'])
def obtener_reservas_por_servicio(id_servicio):
    try:
        controller = ControladorReservas()
        return controller.obtener_reservas_por_servicio(id_servicio)
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

@reservas_bp.route('/api/v1.0/servicios/<int:id_servicio>/reservas/<int:id_reserva>', methods=['DELETE'])
def eliminar_reservas_por_servicio(id_servicio, id_reserva):
    try:
        has_access = Security.verify_token(request.headers)
        if has_access:
            id_usuario_token = has_access.get('id_usuario')
            roles = has_access.get('roles')
            if roles and (TipoRoles.PROVEEDOR.value in roles or TipoRoles.ADMIN.value in roles):
                controller = ControladorReservas()
                return controller.eliminar_reservas_por_servicio(id_servicio, id_reserva, id_usuario_token, roles)
        return jsonify({'message': 'Unauthorized'}), 401
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400
