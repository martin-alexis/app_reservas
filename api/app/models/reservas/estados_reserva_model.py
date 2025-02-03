from api.app import db
from sqlalchemy import  Integer, String
from sqlalchemy.orm import relationship


class EstadosReserva(db.Model):
    __tablename__ = 'estados_reserva'
    id_estados_reserva = db.Column(Integer, primary_key=True, autoincrement=True)
    estado = db.Column(String(45), nullable=False)

    reservas = relationship('Reservas', back_populates='estado_reserva')

    def __init__(self, estado):
        self.estado = estado

    def to_json(self):
        return {
            'id_estados_reserva': self.id_estados_reserva,
            'estado': self.estado
        }