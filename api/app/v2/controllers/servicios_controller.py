from marshmallow import ValidationError
from flask import jsonify, request

from api.app import db
from api.app.models.services.disponibilidad_servicios_model import DisponibilidadServicio
from api.app.models.services.servicios_model import Servicios
from api.app.models.services.tipos_servicios_model import TiposServicio
from api.app.models.users.roles_model import TipoRoles
from api.app.models.users.usuarios_model import Usuarios
from api.app.schemas.servicios.schema_filtros_servicios import filtros_servicios_schema
from api.app.schemas.servicios.schema_servicios import ServiciosSchema, servicio_schema, servicios_schema
from api.app.utils.functions_utils import FunctionsUtils
from api.app.utils.responses import APIResponse


class ControladorServicios:

    def __init__(self):
        pass


    def crear_servicio(self, data, id_usuario_token):
        try:
            data_validada = servicio_schema.load(data)

            usuario = FunctionsUtils.existe_registro(id_usuario_token, Usuarios)
            data_validada['usuarios_proveedores_id'] = usuario.id_usuarios

            data_validada = FunctionsUtils.renombrar_campo(data_validada,'tipos_servicio', 'tipos_servicio_id')
            data_validada = FunctionsUtils.renombrar_campo(data_validada,'disponibilidad_servicio', 'disponibilidad_servicio_id')

            ids_tipos_servicio = FunctionsUtils.obtener_ids_de_enums(TiposServicio,TiposServicio.tipo, data_validada['tipos_servicio_id'], 'id_tipos_servicio')
            ids_disponibilidad_servicio = FunctionsUtils.obtener_ids_de_enums(DisponibilidadServicio,DisponibilidadServicio.estado, data_validada['disponibilidad_servicio_id'], 'id_disponibilidad_servicio')

            data_validada = FunctionsUtils.pasar_ids(data_validada, 'tipos_servicio_id', ids_tipos_servicio)
            data_validada = FunctionsUtils.pasar_ids(data_validada, 'disponibilidad_servicio_id', ids_disponibilidad_servicio)


            imagen = request.files['imagen']
            imagen_url = FunctionsUtils.subir_imagen_cloudinary(imagen, id_usuario_token, 'servicios')
            data_validada['imagen'] = imagen_url

            nuevo_servicio = Servicios(**data_validada)
            db.session.add(nuevo_servicio)
            db.session.commit()

            return APIResponse.created()

        except ValidationError as err:
            return APIResponse.validation_error(errors=err.messages)

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

    def actualizar_imagen_servicio(self, id_servicio, id_usuario_token, roles, correo):
        try:
            servicio = Servicios.query.get(id_servicio)

            if not servicio:
                return jsonify({"error": "Servicio no encontrado"}), 404

            if servicio.usuarios_proveedores_id != id_usuario_token and (not roles or TipoRoles.ADMIN.value not in roles):
                return jsonify({"error": "No tienes permiso para modificar esta imagen"}), 403

            imagen = request.files.get('imagen')
            if not imagen:
                return jsonify({"error": "No se envió ninguna imagen"}), 400

            imagen_url = ControladorServicios.subir_imagen_cloudinary(imagen, id_usuario_token, 'servicios')

            servicio.imagen = imagen_url

            db.session.commit()

        except Exception as e:
            db.session.rollback()
            return jsonify({"error": f"Error al actualizar el registro: {str(e)}"}), 500

        finally:
            db.session.close()

        return jsonify({"message": "Imagen del servicio actualizada exitosamente"}), 200


    @staticmethod
    def aplicar_filtros_precio(query, precio_min, precio_max):
        if precio_min and precio_max:
            query = query.filter(Servicios.precio >= float(precio_min), Servicios.precio <= float(precio_max))
        elif precio_min:
            query = query.filter(Servicios.precio >= float(precio_min))
        elif precio_max:
            query = query.filter(Servicios.precio <= float(precio_max))
        return query



