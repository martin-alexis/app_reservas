from marshmallow import post_load
from decimal import Decimal

from api.app import ma
from api.app.pagos.models.pagos_model import Pagos


class PagosSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Pagos  # Asegúrate de importar el modelo Pagos

    id_pagos = ma.auto_field()
    fecha_pago = ma.fields.DateTime(format='%Y-%m-%dT%H:%M:%S')  # Formato ISO 8601
    monto = ma.fields.Decimal(as_string=True)  # Para manejar decimales correctamente
    reservas_id = ma.auto_field()
    estados_pago_id = ma.auto_field()
    usuarios_id = ma.auto_field()

    # Relaciones
    reserva = ma.fields.Nested('ReservasSchema')
    estado_pago = ma.fields.Nested('EstadosPagoSchema')
    usuario = ma.fields.Nested('UsuariosSchema')

    @post_load
    def make_pago(self, data, **kwargs):
        # Convertir el monto a Decimal si es necesario
        if 'monto' in data and isinstance(data['monto'], str):
            data['monto'] = Decimal(data['monto'])
        return Pagos(**data)

# Instancias del esquema para serialización
pago_schema = PagosSchema()
pagos_schema = PagosSchema(many=True)