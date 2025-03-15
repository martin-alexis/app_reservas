from marshmallow import post_load
from api.app import ma
from api.app.models.services.servicios_model import Servicios

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
    # tipos_servicio_id = ma.auto_field()
    # usuarios_proveedores_id = ma.auto_field()
    # disponibilidad_servicio_id = ma.auto_field()

    tipo_servicio = ma.Nested(TiposServicioSchema)
    # proveedor = ma.Nested(UsuariosSchema)
    disponibilidad = ma.Nested(DisponibilidadServicioSchema)
    # reservas = ma.List(ma.Nested(ReservasSchema))
    usuarios_proveedores_id = ma.auto_field()

    # valoraciones = ma.List(ma.Nested('ValoracionesSchema'))

    @post_load
    def make_servicio(self, data, **kwargs):
        return Servicios(**data)


# Instancias del esquema para serialización
# servicio_schema = ServiciosSchema()
# servicios_schema = ServiciosSchema(many=True)