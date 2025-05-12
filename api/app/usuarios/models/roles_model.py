import enum

from api.app import db
from sqlalchemy import Integer, Enum
from sqlalchemy.orm import relationship


class TipoRoles(enum.Enum):
    ADMIN = "ADMIN"
    CLIENTE = "CLIENTE"
    PROVEEDOR = "PROVEEDOR"

class Roles(db.Model):
    __tablename__ = 'roles'
    id_roles = db.Column(Integer, primary_key=True, autoincrement=True)
    tipo = db.Column(Enum(TipoRoles), nullable=False, unique=True)

    usuarios = relationship('UsuariosTieneRoles', back_populates='rol')

    def __init__(self, tipo):
        self.tipo = tipo

    def to_json(self):
        return {
            'id_roles': self.id_roles,
            'tipo': self.tipo.value
        }
