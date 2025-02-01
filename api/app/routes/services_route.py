
from flask import Blueprint, request, jsonify

from api.app.controllers.servicios_controller import ControladorServicios
from api.app.controllers.usuarios_controller import ControladorUsuarios
from api.app.models.users.roles_model import TipoRoles
from api.app.models.users.tipos_usuarios_model import TiposUsuario
from api.app.utils.security import Security

services_bp = Blueprint('services', __name__)


@services_bp.route('api/services', methods=['POST'])
def crear_servicio():
    has_access = Security.verify_token(request.headers)
    roles = has_access.get('roles')
    email = has_access.get('email')

    if has_access and roles and (TipoRoles.PROVEEDOR.value in roles or TipoRoles.ADMIN.value in roles):
        data = request.get_json()
        controller = ControladorServicios()
        return controller.crear_servicio(data, email)
    else:
        response = jsonify({'message': 'Unauthorized'})
        return response, 401


@services_bp.route('/api/services', methods=['GET'])
def obtener_servicios_usuario():
    has_access = Security.verify_token(request.headers)
    email = has_access.get('email')
    roles= has_access.get('roles')

    if has_access and roles and (TipoRoles.PROVEEDOR.value in roles or TipoRoles.ADMIN.value in roles):
        controller = ControladorServicios()
        return controller.obtener_servicios_usuario(email)

    else:
        response = jsonify({'message': 'Unauthorized'})
        return response, 401


@services_bp.route('/api/services/<int:id_services>', methods=['PATCH'])
def actualizar_servicios(id_services):
    has_access = Security.verify_token(request.headers)
    roles= has_access.get('roles')

    if has_access and roles and (TipoRoles.PROVEEDOR.value in roles or TipoRoles.ADMIN.value in roles):
        controller = ControladorServicios()
        return controller.actualizar_servicio(id_services)

    else:
        response = jsonify({'message': 'Unauthorized'})
        return response, 401

@services_bp.route('/api/services/<int:id_services>', methods=['DELETE'])
def eliminar_servicios_usuario(id_services):
    has_access = Security.verify_token(request.headers)
    email = has_access.get('email')
    roles = has_access.get('roles')

    if has_access and roles and (TipoRoles.PROVEEDOR.value in roles or TipoRoles.ADMIN.value in roles):
        controller = ControladorServicios()
        return controller.eliminar_servicios_usuario(id_services, email)

    else:
        response = jsonify({'message': 'Unauthorized'})
        return response, 401