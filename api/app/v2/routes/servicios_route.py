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



# @api.route('/servicios', methods=['POST'])
# def crear_servicio():
#     try:
#         has_access = Security.verify_token(request.headers)
#         if has_access:
#             roles = has_access.get('roles')
#             email = has_access.get('email')
#             id_usuario_token = has_access.get('id_usuario')
#             if roles and (TipoRoles.PROVEEDOR.value in roles or TipoRoles.ADMIN.value in roles):
#                 data = request.form
#                 controller = ControladorServicios()
#                 return controller.crear_servicio(data, email, id_usuario_token)
#         return jsonify({'message': 'Unauthorized'}), 401
#     except Exception as e:
#         return jsonify({'status': 'error', 'message': str(e)}), 400
@api.route('/servicios', methods=['POST'])
@token_required
@roles_required([TipoRoles.PROVEEDOR.value, TipoRoles.ADMIN.value])
def crear_servicio(payload):
    try:
        id_usuario_token = payload.get('id_usuario')
        data = request.form.to_dict()
        controller = ControladorServicios()
        return controller.crear_servicio(data, id_usuario_token)
    except ConnectionError:
        return jsonify({"status": "error", "message": "No se pudo conectar con la base de datos"}), 500

    except TimeoutError:
        return jsonify(
            {"status": "error", "message": "Tiempo de espera agotado al conectar con la base de datos"}), 500
    except SQLAlchemyError as e:
        return jsonify({
            "status": "error",
            "code": 500,
            "message": "Error al conectar con la base de datos",
            "error": str(e)  # Aquí mostrará el error específico de SQLAlchemy
        }), 500
    except Exception as e:
        return APIResponse.error(message=str(e))


def actualizar_usuario(payload, id_usuario):
    try:
        id_usuario_token = payload.get('id_usuario')
        data = request.json
        controller = ControladorUsuarios()
        return controller.actualizar_usuario(id_usuario, id_usuario_token, data)

    except Exception as e:
        return APIResponse.error(error=str(e))

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
