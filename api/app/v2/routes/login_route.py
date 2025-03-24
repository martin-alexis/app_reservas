from flask import Blueprint, request, jsonify

from api.app.v1.controllers.usuarios_controller import ControladorUsuarios
from api.app.models.users.roles_model import Roles
from api.app.utils.security import Security

from api.app.v1 import api


@api.route('/login', methods=['POST'])
def login_jwt():
    try:
        email = request.json.get('email')
        password = request.json.get('password')

        if not email or not password:
            return jsonify({'message': 'Email y contraseña son requeridos'}), 400

        authenticated_user = ControladorUsuarios.obtener_usuario_por_correo(email)

        if not authenticated_user:
            return jsonify({'message': 'Email incorrecto'}), 404

        if not authenticated_user.check_password(password):
            return jsonify({'message': 'Contraseña incorrecta'}), 401

        roles_user = Roles.get_roles_user(authenticated_user)

        jwt_token = Security.create_token(authenticated_user.id_usuarios, authenticated_user.correo, roles_user)

        return jsonify({'token': jwt_token}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

