from marshmallow import post_load
from marshmallow_enum import EnumField

from api.app import ma
from api.app.models.users.roles_model import TipoRoles, Roles


class RolesSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Roles

    id_roles = ma.auto_field()
    tipo = EnumField(TipoRoles, by_value=True)

    @post_load
    def make_role(self, data, **kwargs):
        return Roles(**data)

# # Instancias del esquema
# role_schema = RolesSchema()
# roles_schema = RolesSchema(many=True)
