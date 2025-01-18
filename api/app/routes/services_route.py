
from flask import Blueprint, request, jsonify

from api.app.controllers.services_controller import ServicesController
from api.app.controllers.user_controller import UsersController
from api.app.models.users.roles import RolesType
from api.app.models.users.users_type import UserType
from api.app.utils.security import Security

services_bp = Blueprint('services', __name__)


@services_bp.route('api/services', methods=['POST'])
def create_services():
    has_access = Security.verify_token(request.headers)
    roles = has_access.get('roles')
    email = has_access.get('email')

    if roles and RolesType.PROVEEDOR.value in roles:
        data = request.get_json()
        controller = ServicesController()
        return controller.create_service(data, email)
    else:
        response = jsonify({'message': 'Unauthorized'})
        return response, 401


@services_bp.route('/api/services', methods=['GET'])
def get_services():

    controller = ServicesController()
    return controller.get_services()

@services_bp.route('/api/services/<int:id_services>', methods=['PATCH'])
def update_services(id_services):
    has_access = Security.verify_token(request.headers)

    if has_access:
        controller = ServicesController()
        return controller.update_services(id_services)

    else:
        response = jsonify({'message': 'Unauthorized'})
        return response, 401

