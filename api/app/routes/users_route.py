
from flask import Blueprint, request, jsonify

from api.app.controllers.usuarios_controller import ControladorUsuarios
from api.app.utils.security import Security

user_bp = Blueprint('user', __name__)


@user_bp.route('api/users', methods=['POST'])
def create_user():
    data = request.get_json()
    controller = ControladorUsuarios()
    return controller.crear_usuario(data)

@user_bp.route('api/users', methods=['GET'])
def get_user():
    data = request.get_json()
    controller = ControladorUsuarios()
    return controller.obtener_usuario_por_email(data['correo'])

# Endpoint para obtener información del usuario
@user_bp.route('/api/user/me', methods=['GET'])
def get_user_info():
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

