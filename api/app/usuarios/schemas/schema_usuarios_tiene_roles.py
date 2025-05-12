from marshmallow import post_load
from api.app import ma
from api.app.usuarios.models.usuarios_tiene_roles_model import UsuariosTieneRoles
from api.app.usuarios.schemas.schema_roles import RolesSchema


class UsuariosTieneRolesSchema(ma.SQLAlchemySchema):
    class Meta:
        model = UsuariosTieneRoles

    id_usuarios_tiene_roles = ma.auto_field()
    usuarios_id = ma.auto_field()
    roles_id = ma.auto_field()
    rol = ma.Nested(RolesSchema, attribute="rol")


    @post_load
    def make_usuarios_tiene_roles(self, data, **kwargs):
        return UsuariosTieneRoles(**data)

usuarios_tiene_roles_schema = UsuariosTieneRolesSchema()
usuarios_tiene_roles_schema_many = UsuariosTieneRolesSchema(many=True)
