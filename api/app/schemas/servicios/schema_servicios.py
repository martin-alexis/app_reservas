from decimal import Decimal

from marshmallow import post_load, fields, validate
from api.app import ma
from api.app.models.services.disponibilidad_servicios_model import Estado
from api.app.models.services.servicios_model import Servicios
from api.app.models.services.tipos_servicios_model import Tipo

from api.app.schemas.servicios.schema_tipos_servicios import TiposServicioSchema
from api.app.schemas.usuarios.schema_usuarios import UsuariosSchema
from api.app.schemas.servicios.schema_disponibilidad_servicios import DisponibilidadServicioSchema
from api.app.schemas.reservas.schema_reservas import ReservasSchema



class ServiciosSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Servicios

    id_servicios = ma.auto_field()
    nombre = ma.auto_field()
    descripcion = ma.auto_field()
    precio = ma.auto_field()
    ubicacion = ma.auto_field()
    imagen = ma.auto_field()

    tipos_servicio = fields.String(required=True, load_only=True, validate=validate.OneOf([tipo.value for tipo in Tipo],
                                                                                         error="Tipo de servicio inválido."))
    disponibilidad_servicio = fields.String(required=True, load_only=True, validate=validate.OneOf([estado.value for estado in Estado], error="Disponibilidad de servicio inválida."))

    # tipos_servicio_id = ma.auto_field()
    usuarios_proveedores_id = ma.auto_field(dump_only=True)
    # disponibilidad_servicio_id = ma.auto_field()

    tipo_servicio = fields.Nested(TiposServicioSchema, dump_only=True)
    # proveedor = fields.Nested(UsuariosSchema, dump_only=True)
    disponibilidad = fields.Nested(DisponibilidadServicioSchema, dump_only=True)

    # tipo_servicio = fields.String(required=True, load_only=True, validate=validate.OneOf([tipo.value for tipo in Tipo],error="Tipo de servicio inválido."))
    # disponibilidad_servicio = fields.String(required=True, load_only=True, validate=validate.OneOf([estado.value for estado in Estado], error="Disponibilidad de servicio inválida."))
    # # tipos_servicio_id = ma.auto_field()
    # # usuarios_proveedores_id = ma.auto_field()
    # # disponibilidad_servicio_id = ma.auto_field()
    #
    # tipo_servicio = ma.Nested(TiposServicioSchema, dump_only=True)
    # # proveedor = ma.Nested(UsuariosSchema)
    # disponibilidad = ma.Nested(DisponibilidadServicioSchema, dump_only=True)
    # # reservas = ma.List(ma.Nested(ReservasSchema))
    # usuarios_proveedores_id = ma.auto_field()

    # valoraciones = ma.List(ma.Nested('ValoracionesSchema'))

    # @post_load
    # def make_servicio(self, data, **kwargs):
    #     return Servicios(**data)
    @post_load
    def convertir_decimal_a_float(self, data, **kwargs):
        """Convierte precio de Decimal a float si es necesario."""
        if isinstance(data.get("precio"), Decimal):
            data["precio"] = float(data["precio"])
        return data

#Instancias del esquema para serialización
servicio_schema = ServiciosSchema()
servicios_schema = ServiciosSchema(many=True)