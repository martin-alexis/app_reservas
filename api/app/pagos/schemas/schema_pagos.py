from marshmallow import post_load
from decimal import Decimal

from api.app import ma
from api.app.pagos.models.pagos_model import Pagos


class PagosSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Pagos  # Asegúrate de importar el modelo Pagos

    id_pagos = ma.auto_field()
    fecha_pago = ma.auto_field(dump_only=True)
    monto = ma.auto_field()  
    reservas_id = ma.auto_field(dump_only=True)
    estados_pago_id = ma.auto_field(dump_only=True)
    usuarios_id = ma.auto_field(dump_only=True)


    @post_load
    def make_pago(self, data, **kwargs):
        # Convertir el monto a Decimal si es necesario
        if 'monto' in data and isinstance(data['monto'], str):
            data['monto'] = Decimal(data['monto'])
        return data

# Instancias del esquema para serialización
pago_schema = PagosSchema()
pagos_schema = PagosSchema(many=True)