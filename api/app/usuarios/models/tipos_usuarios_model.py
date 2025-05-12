import enum

from flask import jsonify

from api.app import db
from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.orm import relationship

class Tipo(enum.Enum):
    PARTICULAR = "PARTICULAR"
    EMPRESA = "EMPRESA"

class TiposUsuario(db.Model):
    __tablename__ = 'tipos_usuario'
    id_tipos_usuario = db.Column(Integer, primary_key=True, autoincrement=True)
    tipo = db.Column(Enum(Tipo), nullable=False)
    usuarios = relationship('Usuarios', back_populates='tipo_usuario')

    def __init__(self, tipo):
        self.tipo = tipo

    def to_json(self):
        return {
            'id_tipos_usuario': self.id_tipos_usuario,
            'tipo': self.tipo.value
        }

