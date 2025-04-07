from flask import jsonify, request
from sqlalchemy.exc import SQLAlchemyError

from api.app.models.users.roles_model import TipoRoles
from api.app.utils.responses import APIResponse
from api.app.utils.security import token_required, roles_required
from api.app.v2 import api
from api.app.utils import common_routes as common
from api.app.v2.controllers.servicios_controller import ControladorServicios


@api.route('/servicios/<int:id_servicio>', methods=['GET'])
def obtener_servicio_id (id_servicio):
       return common.obtener_servicio_por_id(id_servicio)


@api.route('/servicios', methods=['POST'])
@token_required
@roles_required([TipoRoles.PROVEEDOR.value, TipoRoles.ADMIN.value])
def crear_servicio(payload):
    try:
        id_usuario_token = payload.get('id_usuario')
        data = request.form.to_dict()
        controller = ControladorServicios()
        return controller.crear_servicio(data, id_usuario_token)
    except Exception as e:
        return APIResponse.error(message=str(e))



@api.route('/usuarios/<int:id_usuario>/servicios', methods=['GET'])
def obtener_servicios_usuario(id_usuario):
    try:
        has_access = Security.verify_token(request.headers)
        if has_access:
            email = has_access.get('email')
            roles = has_access.get('roles')
            if roles and (TipoRoles.PROVEEDOR.value in roles or TipoRoles.ADMIN.value in roles):
                controller = ControladorServicios()
                return controller.obtener_servicios_usuario(id_usuario)
        return jsonify({'message': 'Unauthorized'}), 401
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

@api.route('/servicios', methods=['GET'])
def obtener_todos_servicios():
    try:
        controller = ControladorServicios()
        return controller.obtener_todos_servicios()
    except Exception as e:
        return APIResponse.error(error=str(e))



@api.route('/servicios/<int:id_servicio>', methods=['PATCH'])
@token_required
@roles_required([TipoRoles.PROVEEDOR.value, TipoRoles.ADMIN.value])
def actualizar_servicios(payload, id_servicio):
    try:
        id_usuario_token = payload.get('id_usuario')
        data = request.json
        controller = ControladorServicios()
        return controller.actualizar_servicio(data, id_usuario_token, id_servicio)
    except Exception as e:
        return APIResponse.error(message=str(e))

@api.route('/servicios/<int:id_servicio>/imagen-servicio', methods=['PUT'])
def actualizar_imagen_servicio(id_servicio):
    try:
        has_access = Security.verify_token(request.headers)

        if has_access:
            id_usuario_token= has_access.get('id_usuario')
            email= has_access.get('email')
            roles = has_access.get('roles')
            controller = ControladorServicios()
            return controller.actualizar_imagen_servicio(id_servicio, id_usuario_token, roles, email)
        else:
            return jsonify({'message': 'Unauthorized'}), 401
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400


@api.route('/servicios/<int:id_servicio>', methods=['DELETE'])
@token_required
@roles_required([TipoRoles.PROVEEDOR.value, TipoRoles.ADMIN.value])
def eliminar_servicios(payload, id_servicio):
    try:
        id_usuario_token = payload.get('id_usuario')
        controller = ControladorServicios()
        return controller.eliminar_servicio(id_usuario_token, id_servicio)
    except Exception as e:
        return APIResponse.error(message=str(e))