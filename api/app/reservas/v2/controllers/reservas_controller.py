from marshmallow import ValidationError

from api.app import db
from api.app.reservas.models.estados_reserva_model import EstadosReserva
from api.app.reservas.models.reservas_model import Reservas
from api.app.servicios.models.disponibilidad_servicios_model import DisponibilidadServicio, Estado
from api.app.servicios.models.servicios_model import Servicios
from api.app.reservas.schemas.schema_reservas import reserva_schema, reserva_partial_schema
from api.app.utils.functions_utils import FunctionsUtils
from api.app.utils.responses import APIResponse


class ControladorReservas:

    def __init__(self):
        pass

    @staticmethod
    def verificar_disponibilidad_rango(data_validada):
        id_servicio = data_validada['servicios_id']
        nueva_fecha_inicio = data_validada['fecha_inicio_reserva']
        nueva_fecha_fin = data_validada['fecha_fin_reserva']

        # Busca si ya existe una reserva que se solape con el nuevo rango
        # Condición 1: es del mismo servicio
        # Condición 2: la reserva existente comienza antes de que termine la nueva
        # Condición 3: la reserva existente termina después de que comienza la nueva
        # Si se cumplen todas esas condiciones, hay conflicto de horario
        conflicto = Reservas.query.filter(
            Reservas.servicios_id == id_servicio,
            Reservas.fecha_inicio_reserva < nueva_fecha_fin,
            Reservas.fecha_fin_reserva > nueva_fecha_inicio
        ).first()

        if conflicto:
            raise PermissionError("Ya existe una reserva en ese horario.")

    @staticmethod
    def verificar_disponibilidad_servicio(servicio):
        disponibilidad = DisponibilidadServicio.query.filter_by(id_disponibilidad_servicio=servicio.disponibilidad_servicio_id).first()
        if disponibilidad.estado.value in [Estado.AGOTADO.value, Estado.PROXIMAMENTE.value]:
            raise PermissionError("No es posible realizar esta accion. El servicio debe estar disponible.")


    def crear_reservas(self, data, id_usuario_token, id_servicio):
        try:
            data_validada = reserva_schema.load(data)

            servicio = FunctionsUtils.existe_registro(id_servicio, Servicios)
            data_validada['servicios_id'] = servicio.id_servicios

            FunctionsUtils.verificar_permisos(servicio, id_usuario_token)
            self.verificar_disponibilidad_servicio(servicio)
            data_validada = FunctionsUtils.renombrar_campo(data_validada,'estados_reserva', 'estados_reserva_id')

            ids_estados_reserva= FunctionsUtils.obtener_ids_de_enums(EstadosReserva,EstadosReserva.estado, data_validada['estados_reserva_id'], 'id_estados_reserva')

            data_validada = FunctionsUtils.pasar_ids(data_validada, 'estados_reserva_id', ids_estados_reserva)

            self.verificar_disponibilidad_rango(data_validada)

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
            self.verificar_disponibilidad_servicio(servicio)
            data_validada = FunctionsUtils.renombrar_campo(data_validada, 'estados_reserva', 'estados_reserva_id')

            ids_estados_reserva = FunctionsUtils.obtener_ids_de_enums(EstadosReserva, EstadosReserva.estado,
                                                                      data_validada['estados_reserva_id'],
                                                                      'id_estados_reserva')

            data_validada = FunctionsUtils.pasar_ids(data_validada, 'estados_reserva_id', ids_estados_reserva)

            self.verificar_disponibilidad_rango(data_validada)

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

