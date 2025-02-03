
from flask import Blueprint, request, jsonify

from api.app.controllers.usuarios_controller import ControladorUsuarios
from api.app.utils.security import Security

user_bp = Blueprint('user', __name__)


@user_bp.route('api/users', methods=['POST'])
def crear_usuario():
    data = request.get_json()
    controller = ControladorUsuarios()
    return controller.crear_usuario(data)

@user_bp.route('api/users', methods=['GET'])
def obtener_usuario_por_correo():
    data = request.get_json()
    controller = ControladorUsuarios()
    return controller.obtener_usuario_por_correo(data['correo'])

@user_bp.route('/api/users/<int:id_usuario>', methods=['PATCH'])
def actualizar_usuario(id_usuario):
    has_access = Security.verify_token(request.headers)
    email = has_access.get('email')

    if has_access:
        controller = ControladorUsuarios()
        return controller.actualizar_usuario(id_usuario, email)

    else:
        response = jsonify({'message': 'Unauthorized'})
        return response, 401

@user_bp.route('/api/users/<int:id_usuario>', methods=['DELETE'])
def eliminar_servicios_usuario(id_usuario):
    has_access = Security.verify_token(request.headers)
    email = has_access.get('email')
    roles = has_access.get('roles')

    if has_access and roles and (TipoRoles.PROVEEDOR.value in roles or TipoRoles.ADMIN.value in roles):
        controller = ControladorServicios()
        return controller.eliminar_servicios_usuario(id_services, email)

    else:
        response = jsonify({'message': 'Unauthorized'})
        return response, 401

# Endpoint para obtener información del usuario
@user_bp.route('/api/user/me', methods=['GET'])
def obtener_info_usuario():
    try:
        # Verifica el token y obtiene la información del usuario
        user_data = Security.verify_token(request.headers)

        if user_data:
            controller = ControladorUsuarios()
            return controller.obtener_info_usuario(user_data)
        else:
            response = jsonify({'message': 'Unauthorized'})
            return response, 401
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

