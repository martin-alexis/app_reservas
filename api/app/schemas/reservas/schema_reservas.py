from marshmallow import post_load, fields, validate

from api.app import ma
from api.app.models.reservas.estados_reserva_model import EstadosReserva, EstadoReserva
from api.app.models.reservas.reservas_model import Reservas


class ReservasSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Reservas

    id_reservas = ma.auto_field()
    fecha_creacion_reserva = ma.auto_field()
    fecha_inicio_reserva = ma.auto_field()
    fecha_fin_reserva = ma.auto_field()
    monto_total = ma.auto_field()
    servicios_id = ma.auto_field(dump_only=True)
    estados_reserva = fields.String(
        required=True,
        load_only=True,
        validate=validate.OneOf([estado.value for estado in EstadoReserva])
    )

    estado_reserva = fields.Nested(EstadosReserva, dump_only=True)



# Instancias del esquema para serialización
reserva_partial_schema = ReservasSchema(partial=True)
reserva_schema = ReservasSchema()
reservas_schema = ReservasSchema(many=True)