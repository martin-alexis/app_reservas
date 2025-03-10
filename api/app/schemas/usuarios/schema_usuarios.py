from marshmallow import post_load
from marshmallow_sqlalchemy import auto_field

from api.app import ma
from api.app.models.users.usuarios_model import Usuarios


class UsuariosSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Usuarios

    id_usuarios = ma.auto_field()
    nombre = ma.auto_field()
    correo = ma.auto_field()
    telefono = ma.auto_field()
    imagen = ma.auto_field()
    tipo_usuario = ma.Nested('TiposUsuarioSchema')
    roles = ma.List(ma.Nested('RolesSchema'))

    @post_load
    def make_user(self, data, **kwargs):
        return Usuarios(**data)

# Instancias del esquema para serialización
usuario_schema = UsuariosSchema()
usuarios_schema = UsuariosSchema(many=True)
