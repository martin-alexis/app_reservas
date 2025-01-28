import enum

from api.app import db
from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from sqlalchemy.orm import relationship


class Tipo(enum.Enum):
    INDUMENTARIA = "INDUMENTARIA"
    VEHICULOS = "VEHICULOS"
    ALOJAMIENTO = "ALOJAMIENTO"

class TiposServicio(db.Model):
    __tablename__ = 'tipos_servicio'
    id_tipos_servicio = db.Column(Integer, primary_key=True, autoincrement=True)
    tipo = db.Column(Enum(Tipo), nullable=False)
    servicios = relationship('Servicios', back_populates='tipo_servicio')

    def __init__(self, tipo):
        self.tipo = tipo

    def to_json(self):
        return {
            'id_tipos_servicio': self.id_tipos_servicio,
            'tipo': self.tipo
        }
