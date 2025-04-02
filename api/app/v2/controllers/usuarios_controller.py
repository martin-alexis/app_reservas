from flask import jsonify, request
from marshmallow import ValidationError
from api.app import db
from api.app.schemas.usuarios.schema_usuarios import UsuariosSchema
from api.app.utils.functions_utils import FunctionsUtils
from api.app.utils.responses import APIResponse
from api.app.models.users.roles_model import Roles, TipoRoles
from api.app.models.users.usuarios_model import Usuarios
from api.app.models.users.usuarios_tiene_roles_model import UsuariosTieneRoles
from api.app.models.users.tipos_usuarios_model import TiposUsuario


class ControladorUsuarios:

    def __init__(self):
        pass

    @staticmethod
    def validar_campos_unicos(data, id_usuario_token=None):
        if 'correo' in data:
            usuario = Usuarios.query.filter_by(correo=data['correo']).first()
            if usuario and usuario.id_usuarios != id_usuario_token:
                raise ValidationError("El correo ya está registrado.")
        if 'telefono' in data:
            usuario = Usuarios.query.filter_by(telefono=data['telefono']).first()
            if usuario and usuario.id_usuarios != id_usuario_token:
                raise ValidationError("El teléfono ya está registrado.")

    @staticmethod
    def eliminar_roles_en_data(data_validada):
        data_con_roles = data_validada.copy()
        data_validada.pop('tipo_roles', None)
        return data_con_roles, data_validada

    @staticmethod
    def renombrar_tipos_usuario(data_validada):
        if 'tipos_usuario' in data_validada:
            data_validada['tipos_usuario_id'] = data_validada.pop('tipos_usuario')
        return data_validada

    @staticmethod
    def existe_usuario(id_usuario):
        usuario = Usuarios.query.get(id_usuario)
        if usuario is None:
            raise ValueError("Usuario")
        return usuario

    @staticmethod
    def existe_imagen(imagen):
        if imagen is None:
            raise ValueError("La imagen no ha sido proporcionada.")
        return imagen

    @staticmethod
    def verificar_permisos(usuario, id_usuario_token):
        roles = FunctionsUtils.get_roles_user(usuario)
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
            data_validada = FunctionsUtils.renombrar_campo(data_validada, 'tipos_usuario', 'tipos_usuario_id')

            ids_tipos_usuarios = FunctionsUtils.obtener_ids_de_enums(TiposUsuario, TiposUsuario.tipo, data_validada['tipos_usuario_id'], 'id_tipos_usuario')
            ids_roles = FunctionsUtils.obtener_ids_de_enums(Roles, Roles.tipo, data_validada['tipo_roles'], 'id_roles')
            data_validada = FunctionsUtils.pasar_ids(data_validada, 'tipos_usuario_id', ids_tipos_usuarios)
            data_validada = FunctionsUtils.pasar_ids(data_validada, 'tipo_roles', ids_roles)

            data_con_roles, data_validada = self.eliminar_roles_en_data(data_validada)

            # Imagen por default
            data_validada.setdefault('imagen',
                                     'https://res.cloudinary.com/dfnjifn4w/image/upload/v1740232796/525e350a-f2e9-4b04-9cf8-93d54bffc2ec.png')

            # Crear usuario
            nuevo_usuario = Usuarios(**data_validada)
            db.session.add(nuevo_usuario)
            db.session.flush()

            # Se asigna los roles
            for rol in data_con_roles['tipo_roles']:
                rol_usuario = UsuariosTieneRoles(usuarios_id=nuevo_usuario.id_usuarios, roles_id=rol)
                db.session.add(rol_usuario)

            db.session.commit()
            return APIResponse.created()

        except ValidationError as err:
            return APIResponse.validation_error(errors=err.messages)

        except Exception as e:
            db.session.rollback()
            return APIResponse.error(error=str(e), code=500)

        finally:
            db.session.close()

    def actualizar_foto_perfil_usuario(self, id_usuario, id_usuario_token):
        try:
            usuario = self.existe_usuario(id_usuario)
            self.verificar_permisos(usuario, id_usuario_token)

            imagen = self.existe_imagen(request.files.get('imagen'))
            imagen_url = FunctionsUtils.subir_imagen_cloudinary(imagen, id_usuario_token, 'usuarios')

            usuario.imagen = imagen_url

            db.session.commit()
            return APIResponse.success()

        except ValueError as e:
            return APIResponse.error(error=str(e))

        except PermissionError as e:
            return APIResponse.forbidden(error=str(e))

        except Exception as e:
            db.session.rollback()
            return APIResponse.error(error=str(e), code=500)

        finally:
            db.session.close()

    def actualizar_usuario(self, id_usuario, id_usuario_token, data):
        try:
            # Validar y deserializar con Marshmallow
            usuario_schema = UsuariosSchema(partial=True)
            data_validada = usuario_schema.load(data)

            usuario = self.existe_usuario(id_usuario)

            self.verificar_permisos(usuario, id_usuario_token)

            self.validar_campos_unicos(data, id_usuario_token)

            # Convertir strings a IDs
            data_validada = FunctionsUtils.renombrar_campo(data_validada, 'tipos_usuario', 'tipos_usuario_id')

            ids_tipos_usuarios = FunctionsUtils.obtener_ids_de_enums(TiposUsuario, TiposUsuario.tipo, data_validada['tipos_usuario_id'], 'id_tipos_usuario')
            ids_roles = FunctionsUtils.obtener_ids_de_enums(Roles, Roles.tipo, data_validada['tipo_roles'], 'id_roles')

            data_validada = FunctionsUtils.pasar_ids(data_validada, 'tipos_usuario_id', ids_tipos_usuarios)
            data_validada = FunctionsUtils.pasar_ids(data_validada, 'tipo_roles', ids_roles)


            data_con_roles, data_validada = self.eliminar_roles_en_data(data_validada)

            # Actualizar solo los campos presentes en los datos validados
            for key, value in data_validada.items():
                setattr(usuario, key, value)

            # Actualización de roles
            if 'tipo_roles' in data:
                roles = data_con_roles['tipo_roles']

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
            return APIResponse.error(error=str(e), code=500)

        finally:
            db.session.close()
