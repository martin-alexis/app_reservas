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
from api.app.schemas.reservas.schema_reservas import reserva_schema
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

    def obtener_servicios_usuario(self, id_usuario):
        try:
            usuario = Usuarios.query.get(id_usuario)
            if not usuario:
                return jsonify({"error": "Usuario no encontrado"}), 404

            servicios = Servicios.query.filter_by(usuarios_proveedores_id=usuario.id_usuarios).all()

            if servicios:
                return jsonify([servicio.to_json() for servicio in servicios]), 200
            else:
                return jsonify({'message': 'No hay servicios registrados.'}), 200

        except Exception as e:
            return jsonify({'error': 'Ocurrió un error al obtener los servicios.', 'message': str(e)}), 500

    def obtener_todos_servicios(self):
        try:

            filtros = filtros_servicios_schema.load(request.args)

            page = filtros["page"]
            per_page = filtros["per_page"]
            precio_min = filtros.get("precio_min")
            precio_max = filtros.get("precio_max")
            tipos_servicios = filtros.get("tipos")
            disponibilidad = filtros.get("disponibilidad")
            busqueda = filtros.get("busqueda")

            query = Servicios.query

            if tipos_servicios:
                query = query.join(TiposServicio).filter(TiposServicio.tipo.in_(tipos_servicios))

            if disponibilidad:
                query = query.join(DisponibilidadServicio).filter(DisponibilidadServicio.estado.in_(disponibilidad))

            if precio_max or precio_min:
                query = ControladorServicios.aplicar_filtros_precio(query, precio_min, precio_max)

            if busqueda:
                query = query.filter(
                    (Servicios.nombre.ilike(f"%{busqueda}%")) | (Servicios.descripcion.ilike(f"%{busqueda}%"))
                )

            pagination = query.paginate(page=page, per_page=per_page, error_out=False)

            if pagination.items == []:
                return APIResponse.pagination(page=pagination.page,
                                              per_page=pagination.per_page, total=pagination.total,
                                              pages=pagination.pages, message='No se encontraron servicios')

            return APIResponse.pagination(data=servicios_schema.dump(pagination.items),page=pagination.page, per_page=pagination.per_page, total=pagination.total, pages=pagination.pages)

        except ValidationError as err:
            return APIResponse.validation_error(errors=err.messages)
        except Exception as e:
            return APIResponse.error(error=str(e), code=500)

    def actualizar_servicio(self, data, id_usuario_token, id_servicio):
        try:
            servivio_schema = ServiciosSchema(partial=True)
            data_validada = servivio_schema.load(data)

            servicio = FunctionsUtils.existe_registro(id_servicio, Servicios)

            FunctionsUtils.verificar_permisos(servicio, id_usuario_token)

            # Actualizar solo los campos presentes en los datos validados
            for key, value in data_validada.items():
                setattr(servicio, key, value)

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

    def eliminar_servicio(self, id_usuario_token, id_servicio):
        try:
            servicio = FunctionsUtils.existe_registro(id_servicio, Servicios)
            FunctionsUtils.verificar_permisos(servicio, id_usuario_token)

            db.session.delete(servicio)
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

    def actualizar_imagen_servicio(self, id_usuario_token, id_servicio):
        try:

            servicio = FunctionsUtils.existe_registro(id_servicio, Servicios)
            FunctionsUtils.verificar_permisos(servicio, id_usuario_token)

            imagen = request.files.get('imagen')

            if not imagen:
                return APIResponse.error(error="No se envió ninguna imagen")

            imagen_url = FunctionsUtils.subir_imagen_cloudinary(imagen, id_usuario_token, 'servicios')

            servicio.imagen = imagen_url
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
