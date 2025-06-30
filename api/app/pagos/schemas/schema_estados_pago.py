from api.app import ma
from api.app.pagos.models.estados_pago_model import EstadoPago, EstadosPago
from marshmallow_enum import EnumField

class EstadosPagoSchema(ma.SQLAlchemySchema):
    class Meta:
        model = EstadosPago

    id_estados_pago = ma.auto_field()
    estado = EnumField(EstadoPago, by_value=True)

