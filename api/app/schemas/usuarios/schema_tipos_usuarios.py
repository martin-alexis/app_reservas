from marshmallow import post_load
from marshmallow_enum import EnumField

from api.app import ma
from api.app.models.users.tipos_usuarios_model import TiposUsuario, Tipo


class TiposUsuarioSchema(ma.SQLAlchemySchema):
    class Meta:
        model = TiposUsuario

    id_tipos_usuario = ma.auto_field()
    tipo = EnumField(Tipo, by_value=True)

    @post_load
    def make_tipo_usuario(self, data, **kwargs):
        return TiposUsuario(**data)

# tipo_usuario_schema = TiposUsuarioSchema()
# tipos_usuario_schema = TiposUsuarioSchema(many=True)