from marshmallow import post_load
from marshmallow_enum import EnumField


from api.app import ma
from api.app.models.pagos.estados_pago_model import EstadosPago
from api.app.models.reservas.estados_reserva_model import EstadoReserva


class EstadosPagoSchema(ma.SQLAlchemySchema):
    class Meta:
        model = EstadosPago

    id_estados_pago = ma.auto_field()
    estado = EnumField(EstadoReserva)

    # Relación con Pagos
    pagos = ma.fields.List(ma.fields.Nested('PagosSchema'))

    @post_load
    def make_estado_pago(self, data, **kwargs):
        return EstadosPago(**data)

# Instancias del esquema para serialización
estado_pago_schema = EstadosPagoSchema()
estados_pago_schema = EstadosPagoSchema(many=True)