import enum

from api.app import db
from sqlalchemy import Column, Integer, Enum
from sqlalchemy.orm import relationship


class ServiceStatus(enum.Enum):
    DISPONIBLE = "DISPONIBLE"
    AGOTADO = "AGOTADO"
    PROXIMAMENTE = "PROXIMAMENTE"

class ServiceAvailability(db.Model):
    __tablename__ = 'service_availability'

    id_service_availability = Column(Integer, primary_key=True, autoincrement=True)
    status = Column(Enum(ServiceStatus), nullable=False)


    services = relationship('Services', back_populates='service_availability')

    def to_dict(self):
        return {
            'id_services_availability': self.id_services_availability,
            'status': self.status
        }