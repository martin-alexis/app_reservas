from marshmallow import Marshmallow, post_load
from api.app import ma
from api.app.models.users.usuarios_tiene_roles_model import UsuariosTieneRoles


class UsuariosTieneRolesSchema(ma.SQLAlchemySchema):
    class Meta:
        model = UsuariosTieneRoles

    id_usuarios_tiene_roles = ma.auto_field()
    usuarios_id = ma.auto_field()
    roles_id = ma.auto_field()

    @post_load
    def make_usuarios_tiene_roles(self, data, **kwargs):
        return UsuariosTieneRoles(**data)

# usuarios_tiene_roles_schema = UsuariosTieneRolesSchema()
# usuarios_tiene_roles_schema_many = UsuariosTieneRolesSchema(many=True)
