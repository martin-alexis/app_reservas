from idlelib.iomenu import errors

from flask import jsonify, request
from marshmallow import ValidationError

from api.app import db
from api.app.schemas.usuarios.schema_usuarios import UsuariosSchema
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
    def validar_campos_unicos(data):
        # Validar que el correo no exista
        if Usuarios.query.filter_by(correo=data['correo']).first():
            raise ValidationError("El correo ya está registrado.")

        # Validar que el teléfono no exista
        if Usuarios.query.filter_by(telefono=data['telefono']).first():
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

        if 'roles_id' in data:
            data['roles_id'] = ControladorUsuarios.obtener_roles_ids(data['roles_id'])

        return data


    def crear_usuario(self, data):
        try:
            # Validar campos únicos (correo y teléfono)
            self.validar_campos_unicos(data)

            # Validar y deserializar con Marshmallow
            usuario_schema = UsuariosSchema()
            data_validada = usuario_schema.load(data)

            # Convertir strings a IDs
            data_validada = self.pasar_strings_a_ids(data_validada)

            # Se elimina roles_id ya que el modelo Usuario no tiene el campo
            data_con_roles = data_validada.copy()
            data_validada.pop('roles_id', None)

            # Crear usuario
            nuevo_usuario = Usuarios(**data_validada)
            db.session.add(nuevo_usuario)
            db.session.commit()

            # Se asigna los roles
            for rol in data_con_roles['roles_id']:
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
    # def actualizar_usuario(self, id_usuario, id_usuario_token, roles):
    #     try:
    #         usuario = Usuarios.query.get(id_usuario)
    #
    #         if not usuario:
    #             return jsonify({"error": "Usuario no encontrado"}), 404
    #
    #         # Verificación de permisos
    #         if usuario.id_usuarios != id_usuario_token and (not roles or TipoRoles.ADMIN.value not in roles):
    #             return jsonify({"error": "No tienes permiso para actualizar los datos"}), 403
    #
    #         data = request.json
    #         updated = False  # Para trackear si realmente hay algo que actualizar
    #
    #         # Validaciones y actualizaciones de datos
    #         if 'nombre' in data:
    #             usuario.nombre = data
    #             updated = True  # Indicar que hubo un cambio
    #
    #         if 'correo' in data:
    #             usuario_existente_por_email = Usuarios.query.filter_by(correo=data['correo']).first()
    #
    #             if usuario_existente_por_email:
    #                 return jsonify({'message': 'El correo ya está registrado'}), 400
    #
    #             usuario.correo = data['correo']
    #             updated = True
    #
    #         if 'telefono' in data:
    #             usuario_existente_por_telefono = Usuarios.query.filter_by(telefono=data['telefono']).first()
    #
    #             if usuario_existente_por_telefono:
    #                 return jsonify({'message': 'El teléfono ya está registrado'}), 400
    #
    #             usuario.telefono = data['telefono']
    #             updated = True
    #
    #         if 'contrasena' in data:
    #             usuario.contrasena = usuario.set_password(data['contrasena'])
    #             updated = True
    #
    #         if 'tipos_usuario' in data:
    #             tipo_usuario = TiposUsuario.query.filter_by(tipo=data['tipos_usuario']).first()
    #             if not tipo_usuario:
    #                 return jsonify({'message': 'Tipo de usuario inválido'}), 400
    #
    #             usuario.tipos_usuario_id = tipo_usuario.id_tipos_usuario
    #             updated = True
    #
    #         # Actualización de roles
    #         if 'roles' in data:
    #             roles = data.get('roles', [])
    #
    #             if not isinstance(roles, list):
    #                 roles = [roles]
    #
    #             # Eliminar roles anteriores del usuario
    #             UsuariosTieneRoles.query.filter_by(usuarios_id=usuario.id_usuarios).delete()
    #
    #             # Validar y asignar los nuevos roles
    #             for rol in roles:
    #                 rol = Roles.query.filter_by(tipo=rol).first()
    #
    #                 if not rol:
    #                     return jsonify({'message': f'Rol inválido: {rol}'}), 400
    #
    #                 # Asignar nuevos roles al usuario
    #                 rol_usuario = UsuariosTieneRoles(usuarios_id=usuario.id_usuarios, roles_id=rol.id_roles)
    #                 db.session.add(rol_usuario)
    #
    #             updated = True
    #
    #         if not updated:
    #             return jsonify({'message': 'No hay cambios para actualizar'}), 400
    #
    #         db.session.commit()
    #     except Exception as e:
    #         db.session.rollback()
    #         return jsonify({"error": "Error al actualizar el registro: " + str(e)}), 500
    #
    #     finally:
    #         db.session.close()
    #
    #     return jsonify({"message": "Usuario actualizado exitosamente"}), 200
    #
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