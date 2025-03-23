from marshmallow import post_load, validate, pre_load, ValidationError, fields, validates

from api.app import ma
from api.app.models.users.roles_model import Roles, TipoRoles
from api.app.models.users.tipos_usuarios_model import TiposUsuario, Tipo
from api.app.models.users.usuarios_model import Usuarios
from api.app.schemas.usuarios.schema_roles import RolesSchema
from api.app.schemas.usuarios.schema_tipos_usuarios import TiposUsuarioSchema


class UsuariosSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Usuarios

    id_usuarios = ma.auto_field()
    nombre = ma.auto_field()
    correo = ma.auto_field(validate=validate.Email(error="Correo invalido. Ingresa un correo válido en formato 'usuario@dominio.com'."))

    telefono = ma.auto_field(validate=validate.Regexp(r'^\+?\d{7,15}$',
                                                      error="Telefono invalido. El teléfono solo puede contener entre 7 y 15 dígitos numéricos, con un '+' opcional al inicio."))
    contrasena = fields.Str(load_only=True, required=True)
    imagen = ma.auto_field(required=False)
    tipos_usuario_id = fields.String(required=True, validate=validate.OneOf([tipo.value for tipo in Tipo],
                                                                            error="Tipo de usuario inválido."))
    roles_id = fields.List(
        fields.String(
            load_only=True,
            validate=validate.OneOf([role.value for role in TipoRoles], error="Rol inválido.")
        ),
        required=True,  # Add required=True here to make the entire list required
        validate=validate.Length(min=1, error="Se requiere al menos un rol.")
    )

    tipos_usuario = ma.Nested(TiposUsuarioSchema)
    roles = ma.List(ma.Nested(RolesSchema))

    @post_load
    def make_user(self, data, **kwargs):
        data.setdefault('imagen',
                        'https://res.cloudinary.com/dfnjifn4w/image/upload/v1740232796/525e350a-f2e9-4b04-9cf8-93d54bffc2ec.png')

        # Convertir tipos_usuario_id a su ID real
        if 'tipos_usuario_id' in data:
            tipo_usuario = TiposUsuario.query.filter_by(tipo=data['tipos_usuario_id']).first()
            if tipo_usuario:
                data['tipos_usuario_id'] = tipo_usuario.id_tipos_usuario

        # Convertir roles_id a IDs
        if 'roles_id' in data:
            roles_db = Roles.query.filter(Roles.tipo.in_(data['roles_id'])).all()
            data['roles_id'] = [role.id_roles for role in roles_db]

        # Crear usuario sin roles_id porque el modelo Usuarios no tiene ese campo
        data_con_roles = data.copy()
        data.pop('roles_id', None)

        usuario = Usuarios(**data)
        usuario.roles_id = data_con_roles.get("roles_id", [])

        return usuario


@validates("correo")
def validate_correo(self, value):
    """Verifica si el correo ya existe en la base de datos."""
    if Usuarios.query.filter_by(correo=value).first():
        raise ValidationError("El correo ya está registrado.")


@validates("telefono")
def validate_telefono(self, value):
    """Verifica si el teléfono ya existe en la base de datos."""
    if Usuarios.query.filter_by(telefono=value).first():
        raise ValidationError("El teléfono ya está registrado.")


# Instancias del esquema para serialización
usuario_schema = UsuariosSchema()
usuarios_schema = UsuariosSchema(many=True)
