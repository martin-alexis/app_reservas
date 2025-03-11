from marshmallow import post_load
from marshmallow_enum import EnumField

from api.app import ma
from api.app.models.reservas.estados_reserva_model import EstadosReserva, EstadoReserva


class EstadosReservaSchema(ma.SQLAlchemySchema):
    class Meta:
        model = EstadosReserva

    id_estados_reserva = ma.auto_field()
    estado = EnumField(EstadoReserva)

    # Relación con reservas (con exclusión para evitar referencias circulares)
    reservas = ma.List(ma.Nested('ReservasSchema', exclude=('estado_reserva',)))

    @post_load
    def make_estado_reserva(self, data, **kwargs):
        return EstadosReserva(**data)


# Instancias del esquema para serialización
estado_reserva_schema = EstadosReservaSchema()
estados_reserva_schema = EstadosReservaSchema(many=True)