from api.app.models.users.roles_model import Roles
from api.app.models.users.tipos_usuarios_model import TiposUsuario
from api.app.models.users.usuarios_model import Usuarios
from api.app.models.users.usuarios_tiene_roles_model import UsuariosTieneRoles
from api.app.utils.responses import APIResponse


def get_roles_user(id_usuario):
    try:
        roles_user = []
        user_role_relations = UsuariosTieneRoles.query.filter_by(usuarios_id=id_usuario).all()

        for relation in user_role_relations:
            role = Roles.query.get(relation.roles_id)
            if role:
                role_str = str(role.tipo).replace('TipoRoles.', '')
                roles_user.append(role_str)
                print(roles_user)
        return roles_user
    except Exception as e:
        return APIResponse.error(None, str(e))

# def get_usertype(id_usuario):
#     try:
#         type_user = TiposUsuario.query.filter_by(id_tipos_usuario=id_usuario.tipos_usuario_id).first()
#         return str(type_user.tipo).replace('Tipo.', '')
#     except Exception as e:
#         return APIResponse.error(None, str(e))

def obtener_usuario_por_correo(correo):
        usuario = Usuarios.query.filter_by(correo=correo).first()

        if usuario:
            return usuario
        else:
            return None