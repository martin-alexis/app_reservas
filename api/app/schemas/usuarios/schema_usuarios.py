from marshmallow import post_load, validate, pre_load, ValidationError, fields, validates

from api.app import ma
from api.app.models.users.roles_model import Roles, TipoRoles
from api.app.models.users.tipos_usuarios_model import TiposUsuario, Tipo
from api.app.models.users.usuarios_model import Usuarios
from api.app.schemas.usuarios.schema_roles import RolesSchema
from api.app.schemas.usuarios.schema_tipos_usuarios import TiposUsuarioSchema
from api.app.schemas.usuarios.schema_usuarios_tiene_roles import UsuariosTieneRolesSchema


class UsuariosSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Usuarios

    id_usuarios = ma.auto_field()
    nombre = ma.auto_field()
    correo = ma.auto_field(validate=validate.Email(error="Correo invalido. Ingresa un correo válido en formato 'usuario@dominio.com'."))

    telefono = ma.auto_field(validate=validate.Regexp(r'^\d{7,15}$',
                                                      error="Telefono invalido. El teléfono solo puede contener entre 7 y 15 dígitos numéricos."))
    contrasena = ma.auto_field(
        required=True,
        load_only=True,
        validate=[
            validate.Length(min=8, max=32, error="La contraseña debe tener entre 8 y 32 caracteres."),
            validate.Regexp(
                regex=r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d@$!%*?&]+$",
                error="La contraseña debe contener al menos una letra y un número."
            )
        ]
    )
    imagen = ma.auto_field(required=False)
    tipos_usuario = fields.String(required=True, validate=validate.OneOf([tipo.value for tipo in Tipo],
                                                                            error="Tipo de usuario inválido."))
    tipo_roles = fields.List(
        fields.String(
            load_only=True,
            validate=validate.OneOf([role.value for role in TipoRoles], error="Rol inválido.")
        ),
        required=True,  # Add required=True here to make the entire list required
        validate=validate.Length(min=1, error="Se requiere al menos un rol.")
    )

    tipo_usuario = ma.Nested(TiposUsuarioSchema, dump_only=True)
    roles = fields.List(
        fields.Nested(UsuariosTieneRolesSchema, dump_only=True), dump_only=True)



# Instancias del esquema para serialización
usuario_schema = UsuariosSchema()
usuarios_schema = UsuariosSchema(many=True)
