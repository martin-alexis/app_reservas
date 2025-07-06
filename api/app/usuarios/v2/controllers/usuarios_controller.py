from flask import request
from marshmallow import ValidationError
from api.app import db
from api.app.servicios.models.servicios_model import Servicios
from api.app.usuarios.schemas.schema_usuarios import UsuariosSchema
from api.app.utils.functions_utils import FunctionsUtils
from api.app.utils.responses import APIResponse
from api.app.usuarios.models.roles_model import Roles, TipoRoles
from api.app.usuarios.models.usuarios_model import Usuarios
from api.app.usuarios.models.usuarios_tiene_roles_model import UsuariosTieneRoles
from api.app.usuarios.models.tipos_usuarios_model import TiposUsuario
from api.app.utils.security import Security


class ControladorUsuarios:

    def __init__(self):
        pass

    @staticmethod
    def validar_campos_unicos(data, id_usuario_token=None):
        """
        Valida que los campos 'correo' y 'telefono' sean únicos en la base de datos.
        Si se encuentra un usuario con el mismo correo o teléfono (distinto del usuario actual), lanza ValidationError.

        Parámetros:
        - data (dict): Datos del usuario a validar.
        - id_usuario_token (int, opcional): ID del usuario actual (para permitir actualizarse a sí mismo).
        """
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
        """
        Elimina el campo 'tipo_roles' del diccionario de datos validados y retorna una copia con los roles y otra sin ellos.

        Parámetros:
        - data_validada (dict): Datos validados del usuario.
        Retorna:
        - tuple: (data_con_roles, data_validada_sin_roles)
        """
        data_con_roles = data_validada.copy()
        data_validada.pop('tipo_roles', None)
        return data_con_roles, data_validada

    @staticmethod
    def renombrar_tipos_usuario(data_validada):
        """
        Renombra el campo 'tipos_usuario' a 'tipos_usuario_id' en el diccionario de datos validados.
        Parámetros:
        - data_validada (dict): Datos validados del usuario.
        Retorna:
        - dict: Diccionario actualizado.
        """
        if 'tipos_usuario' in data_validada:
            data_validada['tipos_usuario_id'] = data_validada.pop('tipos_usuario')
        return data_validada

    @staticmethod
    def existe_imagen(imagen):
        """
        Verifica que se haya proporcionado una imagen. Lanza ValueError si no existe.
        Parámetros:
        - imagen: Archivo de imagen (puede ser None).
        Retorna:
        - imagen: El mismo archivo si existe.
        """
        if imagen is None:
            raise ValueError("La imagen no ha sido proporcionada.")
        return imagen

    @staticmethod
    def verificar_servicios(roles_nuevos, usuario):
        """
        Verifica que un usuario pueda dejar de ser proveedor solo si no tiene servicios asociados.
        Si intenta quitar el rol de proveedor y aún tiene servicios, lanza PermissionError.
        Parámetros:
        - roles_nuevos (list): Lista de roles a asignar.
        - usuario (Usuarios): Instancia del usuario.
        Retorna:
        - list: Lista de roles permitidos.
        """
        roles_actuales = FunctionsUtils.get_roles_user(usuario.id_usuarios)
        if TipoRoles.PROVEEDOR.value in roles_actuales:
            if TipoRoles.PROVEEDOR.value not in roles_nuevos:
                servicio = Servicios.query.filter_by(usuarios_proveedores_id=usuario.id_usuarios).first()
                if servicio:
                    raise PermissionError("Tiene que eliminar los servicios para poder dejar de ser proveedor.")
        return roles_nuevos

    def crear_usuario(self, data):
        """
        Crea un nuevo usuario en la base de datos, asignando roles y tipo de usuario.
        Valida los datos, verifica unicidad de correo/teléfono, asigna imagen por defecto y retorna un token JWT.
        Parámetros:
        - data (dict): Datos del usuario a crear.
        Retorna:
        - APIResponse: Respuesta con token JWT o errores de validación.
        """
        try:
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
            roles_user = FunctionsUtils.get_roles_user(nuevo_usuario.id_usuarios)
            token = Security.create_token(nuevo_usuario.id_usuarios, nuevo_usuario.correo, roles_user)
            return APIResponse.created(data={'token': token})

        except ValidationError as err:
            return APIResponse.validation_error(errors=err.messages)

        except Exception as e:
            db.session.rollback()
            return APIResponse.error(error=str(e), code=500)

        finally:
            db.session.close()

    def actualizar_foto_perfil_usuario(self, id_usuario, id_usuario_token):
        """
        Actualiza la foto de perfil de un usuario, subiendo la imagen a Cloudinary.
        Verifica permisos y retorna una respuesta de éxito o error.
        Parámetros:
        - id_usuario (int): ID del usuario a modificar.
        - id_usuario_token (int): ID del usuario autenticado (para permisos).
        Retorna:
        - APIResponse: Respuesta de éxito o error.
        """
        try:
            usuario = FunctionsUtils.existe_registro(id_usuario, Usuarios)
            FunctionsUtils.verificar_permisos(usuario, id_usuario_token)

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
        """
        Actualiza los datos de un usuario existente, permitiendo cambios parciales.
        Valida permisos, unicidad de correo/teléfono, y actualiza roles si corresponde.
        Parámetros:
        - id_usuario (int): ID del usuario a modificar.
        - id_usuario_token (int): ID del usuario autenticado (para permisos).
        - data (dict): Datos a actualizar.
        Retorna:
        - APIResponse: Respuesta de éxito o error.
        """
        try:
            # Validar y deserializar con Marshmallow
            usuario_schema = UsuariosSchema(partial=True)
            data_validada = usuario_schema.load(data)

            usuario = FunctionsUtils.existe_registro(id_usuario, Usuarios)

            FunctionsUtils.verificar_permisos(usuario, id_usuario_token)

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
                roles_nuevos = self.verificar_servicios(roles, usuario)
                # Eliminar roles anteriores
                UsuariosTieneRoles.query.filter_by(usuarios_id=usuario.id_usuarios).delete()

                # Validar y asignar los nuevos roles
                for rol in roles_nuevos:
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
