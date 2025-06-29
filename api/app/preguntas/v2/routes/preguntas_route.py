from flask import request
from api.app.usuarios.models.roles_model import TipoRoles
from api.app.utils.responses import APIResponse
from api.app.preguntas.v2.controllers.preguntas_controller import ControladorPreguntas
from api.app.utils.security import token_required, roles_required

from api.app.blueprints_v2 import api

@api.route('/servicios/<int:id_servicio>/preguntas', methods=['GET'])
def obtener_preguntas_servicio(id_servicio):
    """Obtener todas las preguntas de un servicio específico"""
    try:
        controller = ControladorPreguntas()
        return controller.obtener_preguntas_servicio(id_servicio)
    except Exception as e:
        return APIResponse.error(message=str(e))

@api.route('/servicios/<int:id_servicio>/preguntas', methods=['POST'])
@token_required
@roles_required([TipoRoles.PROVEEDOR.value, TipoRoles.ADMIN.value, TipoRoles.CLIENTE.value])
def crear_preguntas(payload, id_servicio):
    """Crear una nueva pregunta para un servicio"""
    try:
        id_usuario_token = payload.get('id_usuario')
        data = request.json
        controller = ControladorPreguntas()
        return controller.crear_preguntas(data, id_usuario_token, id_servicio)
    except Exception as e:
        return APIResponse.error(message=str(e))

@api.route('/servicios/<int:id_servicio>/preguntas/<int:id_pregunta>/respuestas', methods=['POST'])
@token_required
@roles_required([TipoRoles.PROVEEDOR.value, TipoRoles.ADMIN.value])
def crear_respuestas(payload, id_servicio, id_pregunta):
    """Crear una respuesta para una pregunta específica"""
    try:
        id_usuario_token = payload.get('id_usuario')
        data = request.json
        controller = ControladorPreguntas()
        return controller.crear_respuestas(data, id_usuario_token, id_servicio, id_pregunta)
    except Exception as e:
        return APIResponse.error(message=str(e))

@api.route('/servicios/<int:id_servicio>/preguntas/<int:id_pregunta>', methods=['DELETE'])
@token_required
@roles_required([TipoRoles.PROVEEDOR.value, TipoRoles.ADMIN.value, TipoRoles.CLIENTE.value])
def eliminar_pregunta(payload, id_servicio, id_pregunta):
    """Eliminar una pregunta específica"""
    try:
        id_usuario_token = payload.get('id_usuario')
        controller = ControladorPreguntas()
        return controller.eliminar_pregunta(id_usuario_token, id_servicio, id_pregunta)
    except Exception as e:
        return APIResponse.error(message=str(e))

