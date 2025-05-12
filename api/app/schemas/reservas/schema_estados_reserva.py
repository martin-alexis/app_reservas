from marshmallow import post_load
from marshmallow_enum import EnumField

from api.app import ma
from api.app.models.reservas.estados_reserva_model import EstadoReserva, EstadosReserva

class EstadosReservaSchema(ma.SQLAlchemySchema):
    class Meta:
        model = EstadosReserva

    id_estados_reserva = ma.auto_field()
    estado = EnumField(EstadoReserva, by_value=True)


    @post_load
    def make_estados_reserva(self, data, **kwargs):
        return EstadosReserva(**data)
