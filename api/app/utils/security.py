from functools import wraps

import jwt

import datetime, os, pytz

from dotenv import load_dotenv
from flask import request

from api.app.utils.responses import APIResponse
from api.app.utils.functions_utils import get_roles_user


class Security:
    # Carga las variables de entorno desde el archivo .env
    load_dotenv()

    token_secret = os.getenv('TOKEN_SECRET')
    tz = pytz.timezone("America/Argentina/Buenos_Aires")

    @staticmethod
    def create_token(id_usuario, email, roles,):
        payload = {
            "id_usuario": id_usuario,
            "email": email,
            "roles": roles,
            "exp": datetime.datetime.now(Security.tz) + datetime.timedelta(hours=24),
            "iat": datetime.datetime.now(Security.tz)
        }
        return jwt.encode(payload, Security.token_secret, algorithm="HS256")


    @staticmethod
    def verify_token(headers):
        if 'Authorization' in headers.keys():
            authorization = headers['Authorization']
            encoded_token = authorization.split(" ")[1]

            try:
                # Decodificar el token JWT
                payload = jwt.decode(encoded_token, Security.token_secret, algorithms=["HS256"])
                return payload  # Retorna los datos del usuario
            except jwt.ExpiredSignatureError:
                return None  # Token expirado
            except jwt.InvalidTokenError:
                return None  # Token inválido
        return None  # Si no hay token o es incorrecto

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        headers = request.headers
        if 'Authorization' not in headers:
            return APIResponse.unauthorized(message="No se ha encontrado el token")

        authorization = headers['Authorization']
        try:
            encoded_token = authorization.split(" ")[1]
            payload = jwt.decode(encoded_token, Security.token_secret, algorithms=["HS256"])
        except jwt.ExpiredSignatureError as e:
            return APIResponse.unauthorized(message="Token expirado", error=str(e))
        except jwt.InvalidTokenError as e:
            return APIResponse.unauthorized(message="Token invalido", error=str(e))

        return f(payload, *args, **kwargs)

    return decorated

def roles_required(roles_permitidos):
    def decorator(f):
        @wraps(f)
        def decorated(payload, *args, **kwargs):
            user_roles = get_roles_user(payload.get('id_usuario'))
            if not any(role in user_roles for role in roles_permitidos):
                return APIResponse.forbidden(message='No tienes permiso para acceder a este recurso.')
            return f(payload, *args, **kwargs)
        return decorated
    return decorator
