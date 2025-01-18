from werkzeug.security import generate_password_hash, check_password_hash

from api.app import db
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship



class Users(db.Model):
    __tablename__ = 'users'

    id_users = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(45), nullable=False)
    email = Column(String(45), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    phone = Column(String(45), nullable=False, unique=True)
    user_types_id = Column(Integer, ForeignKey('user_types.id_user_types'), nullable=False)

    user_type = relationship('UserTypes', back_populates='users')
    users_roles = relationship('UsersHasRoles', back_populates='user')
    services = relationship('Services', back_populates='user_provider')
    # ratings = relationship('Ratings', back_populates='user')
    # bookings = relationship('Bookings', back_populates='user')


    @staticmethod
    def set_password(password):
        # Genera un hash de la contraseña y lo guarda
        return generate_password_hash(password)

    def check_password(self, password):
        # Verifica si la contraseña ingresada coincide con el hash guardado
        return check_password_hash(self.password, password)

    def __init__(self, name, email, password, phone, user_types_id):
        self.name = name
        self.email = email
        self.password = Users.set_password(password)
        self.phone = phone
        self.user_types_id = user_types_id

    def to_dict(self):
        return {
            'id_users': self.id_users,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'user_types_id': self.user_types_id
        }