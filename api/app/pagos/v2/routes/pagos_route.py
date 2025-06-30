from flask import request
from api.app.usuarios.models.roles_model import TipoRoles
from api.app.utils.responses import APIResponse
from api.app.pagos.v2.controllers.pagos_controller import ControladorPagos
from api.app.utils.security import token_required, roles_required
from api.app.blueprints_v2 import api

@api.route('/servicios/<int:id_servicio>/reservas/<int:id_reserva>/pagos', methods=['POST'])
@token_required
@roles_required([TipoRoles.CLIENTE.value, TipoRoles.ADMIN.value])
def efectuar_pago(payload, id_servicio, id_reserva):
    try:
        id_usuario_token = payload.get('id_usuario')
        data = request.json
        controller = ControladorPagos()
        return controller.efectuar_pago(data, id_servicio, id_reserva, id_usuario_token)
    except Exception as e:
        return APIResponse.error(message=str(e))

@api.route('/usuarios/<int:id_usuario>/pagos', methods=['GET'])
@token_required
@roles_required([TipoRoles.CLIENTE.value, TipoRoles.PROVEEDOR.value, TipoRoles.ADMIN.value])
def obtener_pagos_del_usuario(payload, id_usuario):
    try:
        id_usuario_token = payload.get('id_usuario')
        controller = ControladorPagos()
        return controller.obtener_pagos_del_usuario(id_usuario, id_usuario_token)
    except Exception as e:
        return APIResponse.error(message=str(e)) 