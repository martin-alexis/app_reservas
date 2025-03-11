from marshmallow import post_load
from marshmallow_enum import EnumField

from api.app import ma
from api.app.models.services.tipos_servicios_model import TiposServicio, Tipo


class TiposServicioSchema(ma.SQLAlchemySchema):
    class Meta:
        model = TiposServicio

    id_tipos_servicio = ma.auto_field()
    tipo = EnumField(Tipo)

    # Relación con servicios (con exclusión para evitar referencias circulares)
    servicios = ma.List(ma.Nested('ServiciosSchema', exclude=('tipo_servicio',)))

    @post_load
    def make_tipo_servicio(self, data, **kwargs):
        return TiposServicio(**data)


# Instancias del esquema para serialización
tipo_servicio_schema = TiposServicioSchema()
tipos_servicio_schema = TiposServicioSchema(many=True)