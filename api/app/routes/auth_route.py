from flask import Blueprint, request, jsonify

from api.app.controllers.usuarios_controller import ControladorUsuarios
from api.app.models.users.roles_model import Roles
from api.app.models.users.tipos_usuarios_model import TiposUsuario
from api.app.utils.security import Security

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/generate_token', methods=['POST'])
def login_jwt():

    email = request.json['email']
    password = request.json['password']

    authenticated_user = ControladorUsuarios.obtener_usuario_por_email(email)

    if authenticated_user and authenticated_user.check_password(password):
        roles_user = Roles.get_roles_user(authenticated_user)

        type_user = TiposUsuario.get_usertype(authenticated_user)
        jwt_token = Security.create_token(authenticated_user.name, authenticated_user.email, roles_user, type_user)

        return jsonify({'token': jwt_token})

    else:
        return jsonify({'message': 'Unauthorized'}), 401
