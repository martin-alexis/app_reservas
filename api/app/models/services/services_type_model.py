import enum

from api.app import db
from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from sqlalchemy.orm import relationship


class SerciceType(enum.Enum):
    INDUMENTARIA = "INDUMENTARIA"
    VEHICULOS = "VEHICULOS"
    ALOJAMIENTO = "ALOJAMIENTO"

class ServiceTypes(db.Model):
    __tablename__ = 'service_types'

    id_service_types = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(Enum(SerciceType), nullable=False)

    services = relationship('Services', back_populates='service_type')

    def to_dict(self):
        return {
            'id_service_types': self.id_service_types,
            'type': self.type
        }
