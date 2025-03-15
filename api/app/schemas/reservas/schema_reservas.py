from marshmallow import post_load

from api.app import ma
from api.app.models.reservas.reservas_model import Reservas


class ReservasSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Reservas

    id_reservas = ma.auto_field()
    fecha_creacion_reserva = ma.auto_field()
    fecha_inicio_reserva = ma.auto_field()
    fecha_fin_reserva = ma.auto_field()
    monto_total = ma.auto_field()
    servicios_id = ma.auto_field()
    estados_reserva_id = ma.auto_field()

    # Relaciones anidadas con exclusiones para evitar referencias circulares
    servicio = ma.Nested('ServiciosSchema', exclude=('reservas',))
    estado_reserva = ma.Nested('EstadosReservaSchema', exclude=('reservas',))
    pagos = ma.List(ma.Nested('PagosSchema', exclude=('reserva',)))

    @post_load
    def make_reserva(self, data, **kwargs):
        return Reservas(**data)


# Instancias del esquema para serialización
reserva_schema = ReservasSchema()
reservas_schema = ReservasSchema(many=True)