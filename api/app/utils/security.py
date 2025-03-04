import jwt

import datetime, os, pytz

from dotenv import load_dotenv

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