from marshmallow import ValidationError
from flask import jsonify, request
from datetime import datetime

from api.app import db
from api.app.preguntas.models.preguntas_model import Preguntas
from api.app.reservas.models.estados_reserva_model import EstadosReserva
from api.app.reservas.models.reservas_model import Reservas
from api.app.servicios.models.servicios_model import Servicios
from api.app.usuarios.models.roles_model import TipoRoles
from api.app.usuarios.models.usuarios_model import Usuarios
from api.app.preguntas.schemas.schema_preguntas import pregunta_schema, preguntas_schema
from api.app.preguntas.schemas.schema_respuestas import respuesta_schema, respuesta_partial_schema
from api.app.reservas.schemas.schema_reservas import reserva_partial_schema
from api.app.utils.functions_utils import FunctionsUtils
from api.app.utils.responses import APIResponse


class ControladorPreguntas:

    def __init__(self):
        pass

    def obtener_preguntas_servicio(self, id_servicio):
        """
        Obtiene todas las preguntas asociadas a un servicio específico.
        :param id_servicio: ID del servicio.
        :return: APIResponse con la lista de preguntas o error.
        """
        try:
            servicio = FunctionsUtils.existe_registro(id_servicio, Servicios)
            
            preguntas= Preguntas.query.filter_by(servicios_id=servicio.id_servicios).all()
            
            return APIResponse.success(data=preguntas_schema.dump(preguntas))

        except ValueError as e:
            return APIResponse.not_found(resource=str(e))

        except Exception as e:
            return APIResponse.error(error=str(e), code=500)

    def crear_preguntas(self, data, id_usuario_token, id_servicio):
        """
        Crea una nueva pregunta para un servicio.
        :param data: Diccionario con los datos de la pregunta.
        :param id_usuario_token: ID del usuario autenticado.
        :param id_servicio: ID del servicio asociado.
        :return: APIResponse con el resultado de la operación.
        """
        try:
            data_validada = pregunta_schema.load(data)

            servicio = FunctionsUtils.existe_registro(id_servicio, Servicios)
            data_validada['servicios_id'] = servicio.id_servicios

            usuario = FunctionsUtils.existe_registro(id_usuario_token, Usuarios)
            data_validada['usuarios_pregunta_id'] = usuario.id_usuarios

            FunctionsUtils.verificar_permisos(servicio, id_usuario_token)

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

    def crear_respuestas(self, data, id_usuario_token, id_servicio, id_pregunta):
        """
        Crea una respuesta para una pregunta específica de un servicio.
        :param data: Diccionario con los datos de la respuesta.
        :param id_usuario_token: ID del usuario autenticado.
        :param id_servicio: ID del servicio asociado.
        :param id_pregunta: ID de la pregunta a responder.
        :return: APIResponse con el resultado de la operación.
        """
        try:
            data_validada = respuesta_schema.load(data)

            servicio = FunctionsUtils.existe_registro(id_servicio, Servicios)

            pregunta = FunctionsUtils.existe_registro(id_pregunta, Preguntas)
            
            usuario = FunctionsUtils.existe_registro(id_usuario_token, Usuarios) 
            
            data_validada['usuarios_respuesta_id'] = usuario.id_usuarios
     

            FunctionsUtils.verificar_permisos_respuesta(servicio, pregunta, id_usuario_token)

            data_validada['fecha_respuesta'] = datetime.now()

            for key, value in data_validada.items():
                setattr(pregunta, key, value)

            db.session.commit()

            return APIResponse.success(message="Respuesta creada exitosamente")

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

    def eliminar_pregunta(self, id_usuario_token, id_servicio, id_pregunta):
        """
        Elimina una pregunta específica de un servicio, validando permisos y relaciones.
        :param id_usuario_token: ID del usuario autenticado.
        :param id_servicio: ID del servicio asociado.
        :param id_pregunta: ID de la pregunta a eliminar.
        :return: APIResponse con el resultado de la operación.
        """
        try:
            servicio = FunctionsUtils.existe_registro(id_servicio, Servicios)

            pregunta = FunctionsUtils.existe_registro(id_pregunta, Preguntas)

            FunctionsUtils.existe_registro(id_usuario_token, Usuarios)

            FunctionsUtils.pregunta_pertenece_servicio(servicio, pregunta)

            FunctionsUtils.verificar_permisos_eliminar_pregunta(servicio, pregunta, id_usuario_token)

            db.session.delete(pregunta)
            db.session.commit()

            return APIResponse.success(message="Pregunta eliminada exitosamente")

        except ValueError as e:
            return APIResponse.not_found(resource=str(e))

        except PermissionError as e:
            return APIResponse.forbidden(error=str(e))

        except Exception as e:
            db.session.rollback()
            return APIResponse.error(error=str(e), code=500)

        finally:
            db.session.close()

    


