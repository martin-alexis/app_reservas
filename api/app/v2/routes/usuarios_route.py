from flask import request, jsonify

from api.app.models.users.roles_model import TipoRoles
from api.app.utils.responses import APIResponse
from api.app.v2.controllers.usuarios_controller import ControladorUsuarios
from api.app.utils.security import roles_required, token_required

from api.app.v2 import api

@api.route('/usuarios', methods=['POST'])
def crear_usuario():
    try:
        data = request.get_json()
        controller = ControladorUsuarios()
        return controller.crear_usuario(data)
    except Exception as e:
        return APIResponse.error(message=str(e))


@api.route('/usuarios/<int:id_usuario>', methods=['PATCH'])
@token_required
@roles_required([TipoRoles.PROVEEDOR.value, TipoRoles.CLIENTE.value, TipoRoles.ADMIN.value])
def actualizar_usuario(payload, id_usuario):
    try:
        id_usuario_token = payload.get('id_usuario')
        data = request.json
        controller = ControladorUsuarios()
        return controller.actualizar_usuario(id_usuario, id_usuario_token, data)

    except Exception as e:
        return APIResponse.error(error=str(e))


@api.route('/usuarios/<int:id_usuario>/foto-perfil', methods=['PUT'])
@token_required
@roles_required([TipoRoles.PROVEEDOR.value, TipoRoles.CLIENTE.value, TipoRoles.ADMIN.value])
def actualizar_foto_perfil_usuario(payload, id_usuario):
    try:
        id_usuario_token = payload.get('id_usuario')
        controller = ControladorUsuarios()
        return controller.actualizar_foto_perfil_usuario(id_usuario, id_usuario_token)

    except Exception as e:
        return APIResponse.error(error=str(e))

#
#
#
# @api.route('usuarios/<int:id_usuario>', methods=['GET'])
# def obtener_usuario_por_id(id_usuario):
#     try:
#         usuario = Usuarios.query.get(id_usuario)
#         if not usuario:
#             return jsonify({"error": "Usuario no encontrado"}), 404
#
#         return jsonify({
#             'status': 'success',
#             'usuario': usuario.to_json()}), 201
#
#     except Exception as e:
#         return jsonify({'status': 'error', 'message': str(e)}), 400
#

