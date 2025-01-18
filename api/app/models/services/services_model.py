from api.app import db
from sqlalchemy import Column, Integer, String, ForeignKey, DECIMAL, Boolean
from sqlalchemy.orm import relationship

class Services(db.Model):
    __tablename__ = 'services'

    id_services = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(45), nullable=False)
    description = Column(String(255), nullable=False)
    price = Column(DECIMAL, nullable=False)
    location = Column(String(45), nullable=False)
    service_availability_id = Column(Integer, ForeignKey('service_availability.id_service_availability'), nullable=False)
    service_types_id = Column(Integer, ForeignKey('service_types.id_service_types'), nullable=False)
    users_providers_id = Column(Integer, ForeignKey('users.id_users'),  nullable=False)

    service_type = relationship('ServiceTypes', back_populates='services')
    user_provider = relationship('Users', back_populates='services')
    service_availability = relationship('ServiceAvailability', back_populates='services')
    # ratings = relationship('Ratings', back_populates='sservice')
    # bookings = relationship('Bookings', back_populates='service')

    def __init__(self, name, description, price, location, service_availability_id, service_types_id, users_providers_id):
        self.name = name
        self.description = description
        self.price = price
        self.location = location
        self.service_availability_id = service_availability_id
        self.service_types_id = service_types_id
        self.users_providers_id = users_providers_id

    def to_dict(self):
        return {
            'id_services': self.id_services,
            'name': self.name,
            'description': self.description,
            'price': float(self.price),
            'location': self.location,
            'available': self.available,
            'service_types_id': self.service_types_id,
            'users_providers_id': self.users_providers_id
        }