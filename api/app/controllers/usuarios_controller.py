from flask import jsonify

from api.app import db
from api.app.models.users.roles_model import Roles
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

            nuevo_usuario = Usuarios(
                nombre=data['nombre'],
                contrasena=data['contrasena'],
                correo=data['correo'],
                telefono=data['telefono'],
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

    @staticmethod
    def obtener_usuario_por_email(correo):
        try:

            usuario = Usuarios.query.filter_by(correo=correo).first()

            if usuario:
                return usuario
            else:
                return None

        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)}), 400

    @staticmethod
    def obtener_info_usuario(usuario_actual):
        try:
            usuario = Usuarios.query.filter_by(correo=usuario_actual['email']).first()
            return jsonify({
                'username': usuario.nombre
            })
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)}), 400
