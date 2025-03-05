import enum

from api.app import db
from sqlalchemy import Integer, Enum
from sqlalchemy.orm import relationship

class TiposEstadoPago(enum.Enum):
    PENDIENTE = "PENDIENTE"
    CONFIRMADO = "CONFIRMADO"
    RECHAZADO = "RECHAZADO"


class EstadosPago(db.Model):
    __tablename__ = 'estados_pago'
    id_estados_pago = db.Column(Integer, primary_key=True, autoincrement=True)
    estado = db.Column(Enum(TiposEstadoPago), nullable=False)

    pagos = relationship('Pagos', back_populates='estado_pago')

    def __init__(self, estado):
        self.estado = estado

    def to_json(self):
        return {
            'id_estados_pago': self.id_estados_pago,
            'estado': self.estado.value
        }