from flask import request, jsonify

from api.app.servicios.v1.controllers.servicios_controller import ControladorServicios
from api.app.servicios.models.servicios_model import Servicios
from api.app.usuarios.models.roles_model import TipoRoles
from api.app.utils.security import Security

from api.app.blueprints_v1 import api

@api.route('/servicios', methods=['POST'])
def crear_servicio():
    try:
        has_access = Security.verify_token(request.headers)
        if has_access:
            roles = has_access.get('roles')
            email = has_access.get('email')
            id_usuario_token = has_access.get('id_usuario')
            if roles and (TipoRoles.PROVEEDOR.value in roles or TipoRoles.ADMIN.value in roles):
                data = request.form
                controller = ControladorServicios()
                return controller.crear_servicio(data, email, id_usuario_token)
        return jsonify({'message': 'Unauthorized'}), 401
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

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
        return jsonify({'status': 'error', 'message': str(e)}), 400

@api.route('/servicios/<int:id_servicio>', methods=['GET'])
def obtener_servicio_por_id(id_servicio):
    try:
        servicio = Servicios.query.get(id_servicio)
        if not servicio:
            return jsonify({"error": "Servicio no encontrado"}), 404

        return jsonify({
            'status': 'success',
            'servicio': servicio.to_json()}), 201

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

@api.route('/servicios/<int:id_servicios>', methods=['PATCH'])
def actualizar_servicios(id_servicios):
    try:
        has_access = Security.verify_token(request.headers)
        if has_access:
            roles = has_access.get('roles')
            email = has_access.get('email')
            if roles and (TipoRoles.PROVEEDOR.value in roles or TipoRoles.ADMIN.value in roles):
                controller = ControladorServicios()
                return controller.actualizar_servicio(id_servicios, email, roles)
        return jsonify({'message': 'Unauthorized'}), 401
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400


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

@api.route('/usuarios/<int:id_usuario>/servicios/<int:id_servicio>', methods=['DELETE'])
def eliminar_servicios_usuario(id_usuario, id_servicio):
    try:
        has_access = Security.verify_token(request.headers)
        if has_access:
            email = has_access.get('email')
            roles = has_access.get('roles')
            if roles and (TipoRoles.PROVEEDOR.value in roles or TipoRoles.ADMIN.value in roles):
                controller = ControladorServicios()
                return controller.eliminar_servicios_usuario(id_usuario, id_servicio, email, roles)
        return jsonify({'message': 'Unauthorized'}), 401
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400
