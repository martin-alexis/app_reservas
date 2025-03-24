from flask import Blueprint, request, jsonify
from marshmallow import ValidationError

from api.app.models.users.usuarios_model import Usuarios
from api.app.schemas.usuarios.schema_login import LoginSchema
from api.app.utils.functions_utils import obtener_usuario_por_correo, get_roles_user
from api.app.utils.responses import APIResponse
from api.app.utils.security import Security

from api.app.v2 import api

def verificar_usuario(data):
    try:
        authenticated_user = obtener_usuario_por_correo(data['correo'])

        if not authenticated_user or not authenticated_user.check_password(data['contrasena']):
            return APIResponse.unauthorized(message='Correo o contraseña incorrectos')

        return authenticated_user
    except Exception as e:
        return APIResponse.error(error=str(e), code=500)


@api.route('/login', methods=['POST'])
def login_jwt():
    try:
        login_schema = LoginSchema()
        login_data = login_schema.load(request.json)

        usuario_verificado = verificar_usuario(login_data)

        # Si verificar_usuario devuelve una respuesta de error, la retornamos directamente
        if not isinstance(usuario_verificado, Usuarios):
            return usuario_verificado

        roles_user = get_roles_user(usuario_verificado.id_usuarios)

        jwt_token = Security.create_token(usuario_verificado.id_usuarios, usuario_verificado.correo, roles_user)

        return APIResponse.success(data={'jwt_token': jwt_token})

    except ValidationError as err:
        return APIResponse.validation_error(errors=err.messages)

    except Exception as e:
        return APIResponse.error(error=str(e))

