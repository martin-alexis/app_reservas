import enum

from api.app import db
from sqlalchemy import Column, Integer, Enum
from sqlalchemy.orm import relationship


class Estado(enum.Enum):
    DISPONIBLE = "DISPONIBLE"
    AGOTADO = "AGOTADO"
    PROXIMAMENTE = "PROXIMAMENTE"

class DisponibilidadServicio(db.Model):
    __tablename__ = 'disponibilidad_servicio'
    id_disponibilidad_servicio = db.Column(Integer, primary_key=True, autoincrement=True)
    estado = db.Column(Estado, nullable=False)

    servicios = relationship('Servicios', back_populates='disponibilidad')

    def __init__(self, estado):
        self.estado = estado

    def to_json(self):
        return {
            'id_disponibilidad_servicio': self.id_disponibilidad_servicio,
            'estado': self.estado
        }