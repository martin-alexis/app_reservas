
from flask import Blueprint, request, jsonify

from api.app.controllers.servicios_controller import ControladorServicios
from api.app.controllers.usuarios_controller import ControladorUsuarios
from api.app.models.users.roles_model import TipoRoles
from api.app.models.users.tipos_usuarios_model import TiposUsuario
from api.app.utils.security import Security

services_bp = Blueprint('services', __name__)


@services_bp.route('api/services', methods=['POST'])
def create_services():
    has_access = Security.verify_token(request.headers)
    roles = has_access.get('roles')
    email = has_access.get('email')

    if roles and TipoRoles.PROVEEDOR.value in roles:
        data = request.get_json()
        controller = ControladorServicios()
        return controller.crear_servicio(data, email)
    else:
        response = jsonify({'message': 'Unauthorized'})
        return response, 401


@services_bp.route('/api/services', methods=['GET'])
def get_services():

    controller = ControladorServicios()
    return controller.obtener_servicios()

@services_bp.route('/api/services/<int:id_services>', methods=['PATCH'])
def update_services(id_services):
    has_access = Security.verify_token(request.headers)

    if has_access:
        controller = ControladorServicios()
        return controller.actualizar_servicio(id_services)

    else:
        response = jsonify({'message': 'Unauthorized'})
        return response, 401

