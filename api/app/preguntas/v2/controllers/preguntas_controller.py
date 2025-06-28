from marshmallow import ValidationError
from flask import jsonify, request

from api.app import db
from api.app.preguntas.models.preguntas_model import Preguntas
from api.app.reservas.models.estados_reserva_model import EstadosReserva
from api.app.reservas.models.reservas_model import Reservas
from api.app.servicios.models.servicios_model import Servicios
from api.app.usuarios.models.roles_model import TipoRoles
from api.app.usuarios.models.usuarios_model import Usuarios
from api.app.preguntas.schemas.schema_preguntas import pregunta_schema
from api.app.reservas.schemas.schema_reservas import reserva_partial_schema
from api.app.utils.functions_utils import FunctionsUtils
from api.app.utils.responses import APIResponse


class ControladorPreguntas:

    def __init__(self):
        pass

    def crear_preguntas(self, data, id_usuario_token, id_servicio):
        try:
            data_validada = pregunta_schema.load(data)

            servicio = FunctionsUtils.existe_registro(id_servicio, Servicios)
            data_validada['servicios_id'] = servicio.id_servicios

            usuario = FunctionsUtils.existe_registro(id_usuario_token, Usuarios)
            data_validada['usuarios_pregunta_id'] = usuario.id_usuarios

            FunctionsUtils.verificar_usuario_pregunta(servicio, id_usuario_token)

            nueva_pregunta = Preguntas(**data_validada)
            db.session.add(nueva_pregunta)
            db.session.commit()

            return APIResponse.created()

        except ValidationError as err:
            return APIResponse.validation_error(errors=err.messages)

        except ValueError as e:
            return APIResponse.not_found(resource=str(e))

        except PermissionError as e:
            return APIResponse.forbidden(error=str(e))

        except Exception as e:
            db.session.rollback()
            return APIResponse.error(error=str(e), code=500)

        finally:
            db.session.close()

    def eliminar_reservas(self, id_usuario_token, id_servicio, id_reserva):
        try:
            servicio = FunctionsUtils.existe_registro(id_servicio, Servicios)
            reserva = FunctionsUtils.existe_registro(id_reserva, Reservas)

            FunctionsUtils.verificar_permisos_reserva(servicio, reserva, id_usuario_token)

            db.session.delete(reserva)
            db.session.commit()

            return APIResponse.success()

        except ValueError as e:
            return APIResponse.not_found(resource=str(e))

        except PermissionError as e:
            return APIResponse.forbidden(error=str(e))

        except Exception as e:
            db.session.rollback()
            return APIResponse.error(error=str(e), code=500)

        finally:
            db.session.close()
    def actualizar_reservas(self, data, id_usuario_token, id_servicio, id_reserva):
        try:
            data_validada = reserva_partial_schema.load(data)

            servicio = FunctionsUtils.existe_registro(id_servicio, Servicios)
            reserva = FunctionsUtils.existe_registro(id_reserva, Reservas)

            FunctionsUtils.verificar_permisos_reserva(servicio, reserva,id_usuario_token)

            # Actualizar solo los campos presentes en los datos validados
            for key, value in data_validada.items():
                setattr(reserva, key, value)

            db.session.commit()
            return APIResponse.success()

        except ValidationError as err:
            return APIResponse.validation_error(errors=err.messages)

        except ValueError as e:
            return APIResponse.not_found(resource=str(e))

        except PermissionError as e:
            return APIResponse.forbidden(error=str(e))

        except Exception as e:
            db.session.rollback()
            return APIResponse.error(error=str(e), code=500)

        finally:
            db.session.close()
            
def actualizar_reservas_por_servicio(self, id_servicio, id_reserva, id_usuario_token, roles):
    try:
        usuario = Usuarios.query.get(id_usuario_token)

        servicio = Servicios.query.get(id_servicio)

        if not usuario:
            return jsonify({"error": "Usuario no encontrado"}), 404

        if not servicio:
            return jsonify({"error": "Servicio no encontrado"}), 404

        if usuario.id_usuarios != servicio.usuarios_proveedores_id and (servicios.usuarios_proveedores_id != id_reserva.servicios_id) and(
                not roles or TipoRoles.ADMIN.value not in roles):
            return jsonify({"error": "No tienes permiso para actualizar la reserva."}), 403

        reserva = Reservas.query.get(id_reserva)

        if not reserva:
            return jsonify({"error": "Reserva no encontrada"}), 404

        data = request.json

        estado_reserva = True
        if 'fecha_inicio_reserva' in data:
            reserva.fecha_inicio_reserva = datetime.strptime(data['fecha_inicio_reserva'], "%d/%m/%Y %H:%M:%S")
        if 'fecha_fin_reserva' in data:
            reserva.fecha_fin_reserva = datetime.strptime(data['fecha_fin_reserva'], "%d/%m/%Y %H:%M:%S")
        if 'monto_total' in data:
            reserva.monto_total = data['monto_total']
        if 'estados_reserva_id' in data:
            estado_reserva = EstadosReserva.query.filter_by(estado=data['estados_reserva_id']).first()
            reserva.estados_reserva_id = estado_reserva.id_estados_reserva
        elif not estado_reserva:
            return jsonify({"error": "Estado de la reserva no es valido."}), 400

        db.session.commit()

        return jsonify({"message": "Reserva actualizado exitosamente"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Error al actualizar el registro: {str(e)}"}), 500

    finally:
        db.session.close()
