from functools import partial
from idlelib.iomenu import errors

from flask import jsonify, request
from marshmallow import ValidationError

from api.app import db
from api.app.schemas.usuarios.schema_usuarios import UsuariosSchema
from api.app.utils.functions_utils import get_roles_user, obtener_usuario_por_correo
from api.app.utils.responses import APIResponse
from api.app.v1.controllers.servicios_controller import ControladorServicios
from api.app.models.services.servicios_model import Servicios
from api.app.models.users.roles_model import Roles, TipoRoles
from api.app.models.users.usuarios_model import Usuarios
from api.app.models.users.usuarios_tiene_roles_model import UsuariosTieneRoles
from api.app.models.users.tipos_usuarios_model import TiposUsuario


class ControladorUsuarios:

    def __init__(self):
        pass

    @staticmethod
    def validar_campos_unicos(data, usuario_token=None):
        if 'correo' in data:
            usuario = Usuarios.query.filter_by(correo=data['correo']).first()
            if usuario and usuario.id_usuarios != usuario_token.id_usuarios:
                raise ValidationError("El correo ya está registrado.")
        if 'telefono' in data:
            usuario = Usuarios.query.filter_by(correo=data['telefono']).first()
            if usuario and usuario.id_usuarios != usuario_token.id_usuarios:
                raise ValidationError("El teléfono ya está registrado.")

    @staticmethod
    def obtener_tipo_usuario_id(tipo_usuario):
        tipo_usuario_db = TiposUsuario.query.filter_by(tipo=tipo_usuario).first()
        return tipo_usuario_db.id_tipos_usuario if tipo_usuario_db else None

    @staticmethod
    def obtener_roles_ids(roles):
        roles_db = Roles.query.filter(Roles.tipo.in_(roles)).all()
        return [role.id_roles for role in roles_db]

    @staticmethod
    def pasar_strings_a_ids(data):
        if 'tipos_usuario_id' in data:
            data['tipos_usuario_id'] = ControladorUsuarios.obtener_tipo_usuario_id(data['tipos_usuario_id'])

        if 'roles' in data:
            data['roles'] = ControladorUsuarios.obtener_roles_ids(data['roles'])

        return data

    @staticmethod
    def eliminar_roles_en_data(data_validada):
        data_con_roles = data_validada.copy()
        data_validada.pop('roles', None)
        return data_con_roles, data_validada

    @staticmethod
    def existe_usuario(id_usuario):
        usuario = Usuarios.query.get(id_usuario)
        if usuario is None:
            raise ValueError("Usuario")
        return usuario

    @staticmethod
    def verificar_permisos(usuario, id_usuario_token):
        roles = get_roles_user(usuario)
        if usuario.id_usuarios != id_usuario_token and (not roles or TipoRoles.ADMIN.value not in roles):
            raise PermissionError("No tienes permisos para realizar esta acción")

    def crear_usuario(self, data):
        try:

            # Validar y deserializar con Marshmallow
            usuario_schema = UsuariosSchema()
            data_validada = usuario_schema.load(data)

            # Validar campos únicos (correo y teléfono)
            self.validar_campos_unicos(data)

            # Convertir strings a IDs
            data_validada = self.pasar_strings_a_ids(data_validada)

            data_con_roles, data_validada = self.eliminar_roles_en_data(data_validada)

            # Crear usuario
            nuevo_usuario = Usuarios(**data_validada)
            db.session.add(nuevo_usuario)
            db.session.commit()

            # Se asigna los roles
            for rol in data_con_roles['roles']:
                rol_usuario = UsuariosTieneRoles(usuarios_id=nuevo_usuario.id_usuarios, roles_id=rol)
                db.session.add(rol_usuario)

            db.session.commit()
            return APIResponse.created()

        except ValidationError as err:
            return APIResponse.validation_error(errors=err.messages)

        except Exception as e:
            db.session.rollback()
            return APIResponse.error(error=str(e))

        finally:
            db.session.close()

# def actualizar_foto_perfil_usuario(self, id_usuario, correo, roles, id_usuario_token):
    #     try:
    #         usuario = Usuarios.query.get(id_usuario)
    #         mismo_usuario = Usuarios.query.filter_by(correo=correo).first()
    #
    #         if not usuario:
    #             return jsonify({"error": "Usuario no encontrado"}), 404
    #
    #         if usuario.id_usuarios != mismo_usuario.id_usuarios and (not roles or TipoRoles.ADMIN.value not in roles):
    #             return jsonify({"error": "No tienes permiso para modificar esta foto"}), 403
    #
    #         imagen = request.files.get('imagen')
    #         if not imagen:
    #             return jsonify({"error": "No se envió ninguna imagen"}), 400
    #
    #         imagen_url = ControladorServicios.subir_imagen_cloudinary(imagen, id_usuario_token, 'usuarios')
    #
    #         usuario.imagen = imagen_url
    #
    #         db.session.commit()
    #
    #     except Exception as e:
    #         db.session.rollback()
    #         return jsonify({"error": "Error al actualizar el registro"}), 500
    #
    #     finally:
    #         db.session.close()
    #
    #     return jsonify({"message": "Foto de perfil del usuario actualizada exitosamente"}), 200
    #
    def actualizar_usuario(self, id_usuario, id_usuario_token, data):
        try:
            # Validar y deserializar con Marshmallow
            usuario_schema = UsuariosSchema(partial=True)
            data_validada = usuario_schema.load(data)

            usuario = self.existe_usuario(id_usuario)

            self.verificar_permisos(usuario, id_usuario_token)

            self.validar_campos_unicos(data, id_usuario_token)

            data_validada = self.pasar_strings_a_ids(data_validada)

            data_con_roles, data_validada = self.eliminar_roles_en_data(data_validada)

            # Actualizar solo los campos presentes en los datos validados
            for key, value in data_validada.items():
                setattr(usuario, key, value)

            # Actualización de roles
            if 'roles' in data:
                roles = data_con_roles['roles']

                # Eliminar roles anteriores
                UsuariosTieneRoles.query.filter_by(usuarios_id=usuario.id_usuarios).delete()

                # Validar y asignar los nuevos roles
                for rol in roles:
                    # Asignar nuevos roles al usuario
                    rol_usuario = UsuariosTieneRoles(usuarios_id=usuario.id_usuarios, roles_id=rol)
                    db.session.add(rol_usuario)


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
            return APIResponse.error(error=str(e))

        finally:
            db.session.close()


    # @staticmethod
    # def obtener_usuario_por_correo(correo):
    #         usuario = Usuarios.query.filter_by(correo=correo).first()
    #
    #         if usuario:
    #             return usuario
    #         else:
    #             return None
    #
    #
    #
    # @staticmethod
    # def obtener_info_usuario(usuario_actual):
    #     try:
    #         usuario = Usuarios.query.filter_by(correo=usuario_actual['email']).first()
    #         return jsonify({
    #             'username': usuario.nombre
    #         })
    #     except Exception as e:
    #         return jsonify({'status': 'error', 'message': str(e)}), 400
    #
    #
    # # @staticmethod
    # # def verificar_acceso_usuario(email):
    # #
    # #     usuario = ControladorUsuarios.obtener_usuario_por_correo(email)
    # #
    # #     usuario_es_valido = Servicios.query.filter_by(usuarios_proveedores_id=usuario.id_usuario).first()
    # #     if not usuario_es_valido:
    # #         return jsonify({"error": "El usuario no ha creado este servicio"}), 403
    #
    # @staticmethod
    # def verificar_usuario_servicio(email, id_servicio):
    #     usuario = ControladorUsuarios().obtener_usuario_por_correo(email)
    #     if not usuario:
    #         return jsonify({"error": "Usuario no encontrado"}), 404
    #
    #     servicio = Servicios.query.get(id_servicio)
    #     if not servicio:
    #         return jsonify({"error": "Servicio no encontrado"}), 404
    #
    #     usuario_es_valido = Servicios.query.filter_by(usuarios_proveedores_id=usuario.id_usuario).first()
    #     if not usuario_es_valido:
    #         return jsonify({"error": "El usuario no ha creado este servicio"}), 403
    #
    #     return usuario, servicio

    # @staticmethod
    # def verificar_datos_unicos(data):
    #     usuario_existente_por_email = ControladorUsuarios.obtener_usuario_por_correo(data['correo'])
    #     usuario_existente_por_telefono = Usuarios.query.filter_by(telefono=data['telefono']).first()
    #
    #     if usuario_existente_por_email or usuario_existente_por_telefono:
    #         return jsonify({'message': 'El correo o el teléfono ya están registrados'}), 400