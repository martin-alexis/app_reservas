from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename

from api.app.controllers.servicios_controller import ControladorServicios
from api.app.models.users.roles_model import TipoRoles
from api.app.utils.security import Security

services_bp = Blueprint('services', __name__)

@services_bp.route('/api/v1.0/servicios', methods=['POST'])
def crear_servicio():
    try:
        has_access = Security.verify_token(request.headers)
        if has_access:
            roles = has_access.get('roles')
            email = has_access.get('email')
            if roles and (TipoRoles.PROVEEDOR.value in roles or TipoRoles.ADMIN.value in roles):
                data = request.form
                controller = ControladorServicios()
                return controller.crear_servicio(data, email)
        return jsonify({'message': 'Unauthorized'}), 401
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

@services_bp.route('/api/v1.0/usuarios/<int:id_usuario>/servicios', methods=['GET'])
def obtener_servicios_usuario(id_usuario):
    try:
        has_access = Security.verify_token(request.headers)
        if has_access:
            email = has_access.get('email')
            roles = has_access.get('roles')
            if roles and (TipoRoles.PROVEEDOR.value in roles or TipoRoles.ADMIN.value in roles):
                controller = ControladorServicios()
                return controller.obtener_servicios_usuario(id_usuario)
        return jsonify({'message': 'Unauthorized'}), 401
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

@services_bp.route('/api/v1.0/servicios', methods=['GET'])
def obtener_todos_servicios():
    try:
        controller = ControladorServicios()
        return controller.obtener_todos_servicios()
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

@services_bp.route('/api/v1.0/servicios/<int:id_servicios>', methods=['PATCH'])
def actualizar_servicios(id_servicios):
    try:
        has_access = Security.verify_token(request.headers)
        if has_access:
            roles = has_access.get('roles')
            email = has_access.get('email')
            if roles and (TipoRoles.PROVEEDOR.value in roles or TipoRoles.ADMIN.value in roles):
                controller = ControladorServicios()
                return controller.actualizar_servicio(id_servicios, email, roles)
        return jsonify({'message': 'Unauthorized'}), 401
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

@services_bp.route('/api/v1.0/usuarios/<int:id_usuario>/servicios/<int:id_servicio>', methods=['DELETE'])
def eliminar_servicios_usuario(id_usuario, id_servicio):
    try:
        has_access = Security.verify_token(request.headers)
        if has_access:
            email = has_access.get('email')
            roles = has_access.get('roles')
            if roles and (TipoRoles.PROVEEDOR.value in roles or TipoRoles.ADMIN.value in roles):
                controller = ControladorServicios()
                return controller.eliminar_servicios_usuario(id_usuario, id_servicio, email, roles)
        return jsonify({'message': 'Unauthorized'}), 401
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400
