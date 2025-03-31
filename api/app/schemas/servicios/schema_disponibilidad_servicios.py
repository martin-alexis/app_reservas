from marshmallow import post_load
from marshmallow_enum import EnumField

from api.app import ma
from api.app.models.services.disponibilidad_servicios_model import DisponibilidadServicio, Estado


class DisponibilidadServicioSchema(ma.SQLAlchemySchema):
    class Meta:
        model = DisponibilidadServicio

    id_disponibilidad_servicio = ma.auto_field()
    estado = EnumField(Estado, by_value=True)

    # # Relación con servicios (con exclusión para evitar referencias circulares)
    # servicios = ma.List(ma.Nested('ServiciosSchema', exclude=('disponibilidad',)))

    @post_load
    def make_disponibilidad(self, data, **kwargs):
        return DisponibilidadServicio(**data)

#
# # Instancias del esquema para serialización
# disponibilidad_schema = DisponibilidadServicioSchema()
# disponibilidades_schema = DisponibilidadServicioSchema(many=True)