from api.app import db
from api.app.pagos.models.estados_pago_model import EstadosPago, TiposEstadoPago
from api.app.pagos.models.pagos_model import Pagos
from api.app.reservas.models.estados_reserva_model import EstadosReserva, EstadoReserva
from api.app.reservas.models.reservas_model import Reservas
from api.app.servicios.models.servicios_model import Servicios
from api.app.usuarios.models.roles_model import TipoRoles
from api.app.usuarios.models.usuarios_model import Usuarios
from api.app.utils.responses import APIResponse
from api.app.utils.functions_utils import FunctionsUtils
from api.app.pagos.schemas.schema_pagos import pago_schema, pagos_schema
from marshmallow import ValidationError

from flask import request

class ControladorPagos:
    def __init__(self):
        pass

    def efectuar_pago(self, data, id_servicio, id_reserva, id_usuario_token):
        try:
            data_validada = pago_schema.load(data)

            servicio = FunctionsUtils.existe_registro(id_servicio, Servicios)

            reserva = FunctionsUtils.existe_registro(id_reserva, Reservas)
            data_validada['reservas_id'] = reserva.id_reservas

            usuario = FunctionsUtils.existe_registro(id_usuario_token, Usuarios)
            data_validada['usuarios_id'] = usuario.id_usuarios

            FunctionsUtils.reserva_pertece_servicio(servicio, reserva)

            FunctionsUtils.verificar_usuario_no_es_proveedor(servicio, usuario)

            FunctionsUtils.verificar_reserva_ya_reservada(reserva)

            FunctionsUtils.verificar_pago_monto_exactitud(servicio, data_validada['monto'])

            FunctionsUtils.poner_reserva_en_estado_reservada(reserva)

            data_validada['estados_pago_id'] = TiposEstadoPago.CONFIRMADO.value

            tipo_pago = FunctionsUtils.obtener_ids_de_enums(EstadosPago, EstadosPago.estado, data_validada['estados_pago_id'], 'id_estados_pago')
            data_validada = FunctionsUtils.pasar_ids(data_validada, 'estados_pago_id', tipo_pago)

            nuevo_pago = Pagos(**data_validada) 
            db.session.add(nuevo_pago)
            db.session.commit()

            return APIResponse.created(message='Pago creado exitosamente')
        
        except ValidationError as err:
            return APIResponse.validation_error(errors=err.messages)

        except ValueError as e:
            return APIResponse.validation_error(errors=str(e))

        except PermissionError as e:
            return APIResponse.forbidden(error=str(e))

        except Exception as e:
            db.session.rollback()
            return APIResponse.error(error=str(e), code=500)

        finally:
            db.session.close()

    def obtener_pagos_del_usuario(self, id_usuario, id_usuario_token):
        try:
            usuario = FunctionsUtils.existe_registro(id_usuario, Usuarios)

            FunctionsUtils.verificar_permisos(usuario, id_usuario_token)
            
            pagos = Pagos.query.filter_by(usuarios_id=usuario.id_usuarios).all()

            return APIResponse.success(data=pagos_schema.dump(pagos))

        except ValueError as e:
            return APIResponse.not_found(resource=str(e))
        
        except Exception as e:
            return APIResponse.error(error=str(e), code=500) 