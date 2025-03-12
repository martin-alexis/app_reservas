from flask import request, jsonify

from api.app.v1.controllers.servicios_controller import ControladorServicios
from api.app.v1.controllers.usuarios_controller import ControladorUsuarios
from api.app.models.users.roles_model import TipoRoles
from api.app.models.users.usuarios_model import Usuarios
from api.app.utils.security import Security

from api.app.v1 import api

@api.route('/usuarios', methods=['POST'])
def crear_usuario():
    try:
        data = request.get_json()
        controller = ControladorUsuarios()
        return controller.crear_usuario(data)
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400


@api.route('/usuarios/<int:id_usuario>', methods=['PATCH'])
def actualizar_usuario(id_usuario):
    try:
        has_access = Security.verify_token(request.headers)
        if has_access:
            id_usuario_token = has_access.get('id_usuario')
            roles = has_access.get('roles')
            controller = ControladorUsuarios()
            return controller.actualizar_usuario(id_usuario, id_usuario_token, roles)
        else:
            return jsonify({'message': 'Unauthorized'}), 401
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400


@api.route('/usuarios/<int:id_usuario>/foto-perfil', methods=['PUT'])
def actualizar_foto_perfil_usuario(id_usuario):
    try:
        has_access = Security.verify_token(request.headers)

        if has_access:
            email = has_access.get('email')
            roles = has_access.get('roles')
            id_usuario_token = has_access.get('id_usuario')
            controller = ControladorUsuarios()
            return controller.actualizar_foto_perfil_usuario(id_usuario, email, roles, id_usuario_token)
        else:
            return jsonify({'message': 'Unauthorized'}), 401
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400


@api.route('/usuarios/<int:id_usuario>', methods=['DELETE'])
def eliminar_servicios_usuario(id_usuario):
    try:
        has_access = Security.verify_token(request.headers)
        email = has_access.get('email')
        roles = has_access.get('roles')

        if has_access and roles and (TipoRoles.PROVEEDOR.value in roles or TipoRoles.ADMIN.value in roles):
            controller = ControladorServicios()
            return controller.eliminar_servicios_usuario(id_usuario, email)
        else:
            return jsonify({'message': 'Unauthorized'}), 401
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400


@api.route('usuarios/<int:id_usuario>', methods=['GET'])
def obtener_usuario_por_id(id_usuario):
    try:
        usuario = Usuarios.query.get(id_usuario)
        if not usuario:
            return jsonify({"error": "Usuario no encontrado"}), 404

        return jsonify({
            'status': 'success',
            'usuario': usuario.to_json()}), 201

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400


# @api.route('/user/me', methods=['GET'])
# def obtener_info_usuario():
#     try:
#         user_data = Security.verify_token(request.headers)
#
#         if user_data:
#             controller = ControladorUsuarios()
#             return controller.obtener_info_usuario(user_data)
#         else:
#             return jsonify({'message': 'Unauthorized'}), 401
#     except Exception as e:
#         return jsonify({'status': 'error', 'message': str(e)}), 400


# @user_bp.route('/usuarios', methods=['GET'])
# def obtener_usuario_por_correo():
#     try:
#         data = request.get_json()
#         controller = ControladorUsuarios()
#         return controller.obtener_usuario_por_correo(data['correo'])
#     except Exception as e:
#         return jsonify({'status': 'error', 'message': str(e)}), 400