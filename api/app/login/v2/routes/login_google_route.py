from datetime import datetime

import requests
from flask import url_for, session, jsonify, redirect, current_app

from api.app.blueprints_v1 import api
from api.app.usuarios.models.usuarios_model import Usuarios
from api.app.utils.responses import APIResponse
from api.app.utils.security import Security, token_required
from api.app.utils.functions_utils import FunctionsUtils

from api.oauth import google, oauth

from api.app.blueprints_v2 import api

import secrets
from flask import session, request

invalidated_tokens = set()

@api.route('/google/login')
def google_login():
    # Generar estado único para CSRF
    state = secrets.token_urlsafe(32)
    session['oauth_state'] = state
    
    return google.authorize_redirect(
        url_for('api_v2.authorize', _external=True),
        state=state
    )

@api.route("/google/callback")
def google_callback():
    try:
        # Verificar estado CSRF
        received_state = request.args.get('state')
        session_state = session.get('oauth_state')
        
        if not received_state or received_state != session_state:
            return APIResponse.error(message="Estado inválido", code=400)
        
        # Limpiar estado después de usar
        session.pop('oauth_state', None)
        
        oauth_token = google.authorize_access_token()
        resp = google.get(google.server_metadata['userinfo_endpoint'])
        
        # Validación mínima del response
        if resp.status_code != 200:
            return APIResponse.unauthorized(message="Error obteniendo datos del usuario", code=401)
        
        user_info = resp.json()
        
        
        user = Usuarios.query.filter_by(correo=user_info['email']).first()
        
        if user:
            
            roles_user = FunctionsUtils.get_roles_user(user.id_usuarios)
            token = Security.create_token(user.id_usuarios, user.correo, roles_user)
            return APIResponse.success(data={'token': token})
        else:
            return APIResponse.success(data={
                "usuario_nuevo": True,
                "google_user": {
                    "nombre": user_info.get("name", ""),
                    "correo": user_info["email"],
                    "picture": user_info.get("picture", "")
                }
            })
    
    except Exception as e:
        return APIResponse.error(message="Error en autenticación", code=500)




@api.route('/google/logout', methods=['POST'])
def google_logout():
    try:
        # Obtener el token del header de autorización
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return APIResponse.error(
                message='Token no proporcionado',
                status_code=401
            )

        token = auth_header.split(' ')[1]
        
        # Agregar el token a la lista de tokens invalidados
        invalidated_tokens.add(token)
        
        return APIResponse.success(message='Sesión cerrada exitosamente')
        
    except Exception as e:
        return APIResponse.error(
            message='Error al cerrar sesión',
            code=500
        )