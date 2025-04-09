from marshmallow import ValidationError
from flask import jsonify, request

from api.app import db
from api.app.models.reservas.estados_reserva_model import EstadoReserva, EstadosReserva
from api.app.models.reservas.reservas_model import Reservas
from api.app.models.services.disponibilidad_servicios_model import DisponibilidadServicio
from api.app.models.services.servicios_model import Servicios
from api.app.models.services.tipos_servicios_model import TiposServicio
from api.app.models.users.roles_model import TipoRoles
from api.app.models.users.usuarios_model import Usuarios
from api.app.schemas.reservas.schema_reservas import reserva_schema, reserva_partial_schema
from api.app.schemas.servicios.schema_filtros_servicios import filtros_servicios_schema
from api.app.schemas.servicios.schema_servicios import ServiciosSchema, servicio_schema, servicios_schema
from api.app.utils.functions_utils import FunctionsUtils
from api.app.utils.responses import APIResponse


class ControladorReservas:

    def __init__(self):
        pass

    def crear_reservas(self, data, id_usuario_token, id_servicio):
        try:
            data_validada = reserva_schema.load(data)

            servicio = FunctionsUtils.existe_registro(id_servicio, Servicios)
            data_validada['servicios_id'] = servicio.id_servicios

            FunctionsUtils.verificar_permisos(servicio, id_usuario_token)

            data_validada = FunctionsUtils.renombrar_campo(data_validada,'estados_reserva', 'estados_reserva_id')

            ids_estados_reserva= FunctionsUtils.obtener_ids_de_enums(EstadosReserva,EstadosReserva.estado, data_validada['estados_reserva_id'], 'id_estados_reserva')

            data_validada = FunctionsUtils.pasar_ids(data_validada, 'estados_reserva_id', ids_estados_reserva)


            nueva_reserva = Reservas(**data_validada)
            db.session.add(nueva_reserva)
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