from datetime import datetime

from api.app import db
from sqlalchemy import DateTime, Integer, Decimal, ForeignKey
from sqlalchemy.orm import relationship


class Pagos(db.Model):
    __tablename__ = 'pagos'
    id_pagos = db.Column(Integer, primary_key=True)
    fecha_pago = db.Column(DateTime, nullable=False)
    monto = db.Column(Decimal(10, 2), nullable=False)
    reservas_id = db.Column(Integer, ForeignKey('reservas.id_reservas'), nullable=False)
    estados_pago_id = db.Column(Integer, ForeignKey('estados_pago.id_estados_pago'), nullable=False)

    reserva = relationship('Reservas', back_populates='pagos')
    estado_pago = relationship('EstadosPago', back_populates='pagos')

    def __init__(self, monto, reservas_id, estados_pago_id):
        self.fecha_pago = datetime.now()
        self.monto = monto
        self.reservas_id = reservas_id
        self.estados_pago_id = estados_pago_id

    def to_json(self):
        return {
            'id_pagos': self.id_pagos,
            'fecha_pago': self.fecha_pago.isoformat(),
            'monto': float(self.monto),
            'reservas_id': self.reservas_id,
            'estados_pago_id': self.estados_pago_id,
            'estado_pago': self.estado_pago.to_json() if self.estado_pago else None,
            'reserva': self.reserva.to_json() if self.reserva else None
        }
