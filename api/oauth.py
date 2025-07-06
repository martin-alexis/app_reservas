"""
Módulo de configuración OAuth para la autenticación social.

Este archivo inicializa la extensión OAuth de Flask y registra el proveedor de Google, utilizando los parámetros de configuración definidos en el proyecto.

- Permite la autenticación de usuarios mediante Google OAuth 2.0/OpenID Connect.
- Centraliza la instancia de OAuth y el cliente de Google para ser reutilizados en los blueprints de login.
- Utiliza los valores de CLIENT_ID y CLIENT_SECRET definidos en la configuración global.

Uso típico:
- Importar `oauth` y `google` en los blueprints de autenticación para iniciar el flujo OAuth y obtener información del usuario autenticado.
"""
from authlib.integrations.flask_client import OAuth

from api.config import Config

# Instancia global de OAuth para la app
oauth = OAuth()

# Cliente de autenticación Google configurado para OAuth 2.0/OpenID Connect
# Utiliza discovery automático de endpoints y scopes básicos (openid, email, profile)
google = oauth.register(
    name='google',
    client_id=Config.CLIENT_ID,
    client_secret=Config.CLIENT_SECRET,
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={
        'scope': (
            'openid email profile '
        )
    }
)
