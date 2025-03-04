from flask import jsonify, request
from pygments.lexer import default

from api.app import db
from api.app.controllers.servicios_controller import ControladorServicios
from api.app.models.services.servicios_model import Servicios
from api.app.models.users.roles_model import Roles, TipoRoles
from api.app.models.users.usuarios_model import Usuarios
from api.app.models.users.usuarios_tiene_roles_model import UsuariosTieneRoles
from api.app.models.users.tipos_usuarios_model import TiposUsuario


class ControladorUsuarios:

    def __init__(self):
        pass

    def crear_usuario(self, data):
        try:
            # Verificar si el correo o el teléfono ya están registrados
            usuario_existente_por_email = Usuarios.query.filter_by(correo=data['correo']).first()
            usuario_existente_por_telefono = Usuarios.query.filter_by(telefono=data['telefono']).first()

            if usuario_existente_por_email or usuario_existente_por_telefono:
                return jsonify({'message': 'El correo o el teléfono ya están registrados'}), 400

            # Obtener el tipo de usuario
            tipo_usuario = TiposUsuario.query.filter_by(tipo=data['tipos_usuario_id']).first()
            if not tipo_usuario:
                return jsonify({'message': 'Tipo de usuario inválido'}), 400

            logo_default_user= 'https://res.cloudinary.com/dfnjifn4w/image/upload/v1740232796/525e350a-f2e9-4b04-9cf8-93d54bffc2ec.png'

            nuevo_usuario = Usuarios(
                nombre=data['nombre'],
                contrasena=data['contrasena'],
                correo=data['correo'],
                telefono=data['telefono'],
                imagen=logo_default_user,
                tipos_usuario_id=tipo_usuario.id_tipos_usuario
            )
            db.session.add(nuevo_usuario)

            # Obtener los roles del usuario
            roles = data.get('roles_id', [])

            if not isinstance(roles, list):
                roles = [roles]

            for rol in roles:
                rol = Roles.query.filter_by(tipo=rol).first()

                if not rol:
                    return jsonify({'message': f'Rol inválido:'}), 400

                # Asignar rol al usuario
                rol_usuario = UsuariosTieneRoles(usuarios_id=nuevo_usuario.id_usuarios, roles_id=rol.id_roles)
                db.session.add(rol_usuario)

            db.session.commit()

            return jsonify({
                'status': 'success',
                'message': 'Usuario creado exitosamente'
                # 'usuario': nuevo_usuario.to_dict(),
                # 'tipo_usuario': tipo_usuario.to_dict(),
                # 'rol': rol.to_dict()
            }), 201


        except Exception as e:
            db.session.rollback()
            return jsonify({'status': 'error', 'message': str(e)}), 400

        finally:
            db.session.close()

    def actualizar_foto_perfil_usuario(self, id_usuario, correo, roles, id_usuario_token):
        try:
            usuario = Usuarios.query.get(id_usuario)
            mismo_usuario = Usuarios.query.filter_by(correo=correo).first()

            if not usuario:
                return jsonify({"error": "Usuario no encontrado"}), 404

            if usuario.id_usuarios != mismo_usuario.id_usuarios and (not roles or TipoRoles.ADMIN.value not in roles):
                return jsonify({"error": "No tienes permiso para modificar esta foto"}), 403

            imagen = request.files.get('imagen')
            if not imagen:
                return jsonify({"error": "No se envió ninguna imagen"}), 400

            imagen_url = ControladorServicios.subir_imagen_cloudinary(imagen, id_usuario_token, 'usuarios')

            usuario.imagen = imagen_url

            db.session.commit()

        except Exception as e:
            db.session.rollback()
            return jsonify({"error": "Error al actualizar el registro"}), 500

        finally:
            db.session.close()

        return jsonify({"message": "Foto de perfil del usuario actualizada exitosamente"}), 200

    def actualizar_usuario(self, id_usuario, id_usuario_token, roles):
        try:
            usuario = Usuarios.query.get(id_usuario)

            if not usuario:
                return jsonify({"error": "Usuario no encontrado"}), 404

            # Verificación de permisos
            if usuario.id_usuarios != id_usuario_token and (not roles or TipoRoles.ADMIN.value not in roles):
                return jsonify({"error": "No tienes permiso para actualizar los datos"}), 403

            data = request.json
            updated = False  # Para trackear si realmente hay algo que actualizar

            # Validaciones y actualizaciones de datos
            if 'nombre' in data:
                usuario.nombre = data['nombre']
                updated = True  # Indicar que hubo un cambio

            if 'correo' in data:
                usuario_existente_por_email = Usuarios.query.filter_by(correo=data['correo']).first()

                if usuario_existente_por_email:
                    return jsonify({'message': 'El correo ya está registrado'}), 400

                usuario.correo = data['correo']
                updated = True

            if 'telefono' in data:
                usuario_existente_por_telefono = Usuarios.query.filter_by(telefono=data['telefono']).first()

                if usuario_existente_por_telefono:
                    return jsonify({'message': 'El teléfono ya está registrado'}), 400

                usuario.telefono = data['telefono']
                updated = True

            if 'contrasena' in data:
                usuario.contrasena = usuario.set_password(data['contrasena'])
                updated = True

            if 'tipos_usuario' in data:
                tipo_usuario = TiposUsuario.query.filter_by(tipo=data['tipos_usuario']).first()
                if not tipo_usuario:
                    return jsonify({'message': 'Tipo de usuario inválido'}), 400

                usuario.tipos_usuario_id = tipo_usuario.id_tipos_usuario
                updated = True

            # Actualización de roles
            if 'roles' in data:
                roles = data.get('roles', [])

                if not isinstance(roles, list):
                    roles = [roles]

                # Eliminar roles anteriores del usuario
                UsuariosTieneRoles.query.filter_by(usuarios_id=usuario.id_usuarios).delete()

                # Validar y asignar los nuevos roles
                for rol in roles:
                    rol = Roles.query.filter_by(tipo=rol).first()

                    if not rol:
                        return jsonify({'message': f'Rol inválido: {rol}'}), 400

                    # Asignar nuevos roles al usuario
                    rol_usuario = UsuariosTieneRoles(usuarios_id=usuario.id_usuarios, roles_id=rol.id_roles)
                    db.session.add(rol_usuario)

                updated = True

            if not updated:
                return jsonify({'message': 'No hay cambios para actualizar'}), 400

            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": "Error al actualizar el registro: " + str(e)}), 500

        finally:
            db.session.close()

        return jsonify({"message": "Usuario actualizado exitosamente"}), 200

    @staticmethod
    def obtener_usuario_por_correo(correo):
            usuario = Usuarios.query.filter_by(correo=correo).first()

            if usuario:
                return usuario
            else:
                return None



    @staticmethod
    def obtener_info_usuario(usuario_actual):
        try:
            usuario = Usuarios.query.filter_by(correo=usuario_actual['email']).first()
            return jsonify({
                'username': usuario.nombre
            })
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)}), 400


    # @staticmethod
    # def verificar_acceso_usuario(email):
    #
    #     usuario = ControladorUsuarios.obtener_usuario_por_correo(email)
    #
    #     usuario_es_valido = Servicios.query.filter_by(usuarios_proveedores_id=usuario.id_usuario).first()
    #     if not usuario_es_valido:
    #         return jsonify({"error": "El usuario no ha creado este servicio"}), 403

    @staticmethod
    def verificar_usuario_servicio(email, id_servicio):
        usuario = ControladorUsuarios().obtener_usuario_por_correo(email)
        if not usuario:
            return jsonify({"error": "Usuario no encontrado"}), 404

        servicio = Servicios.query.get(id_servicio)
        if not servicio:
            return jsonify({"error": "Servicio no encontrado"}), 404

        usuario_es_valido = Servicios.query.filter_by(usuarios_proveedores_id=usuario.id_usuario).first()
        if not usuario_es_valido:
            return jsonify({"error": "El usuario no ha creado este servicio"}), 403

        return usuario, servicio

    # @staticmethod
    # def verificar_datos_unicos(data):
    #     usuario_existente_por_email = ControladorUsuarios.obtener_usuario_por_correo(data['correo'])
    #     usuario_existente_por_telefono = Usuarios.query.filter_by(telefono=data['telefono']).first()
    #
    #     if usuario_existente_por_email or usuario_existente_por_telefono:
    #         return jsonify({'message': 'El correo o el teléfono ya están registrados'}), 400