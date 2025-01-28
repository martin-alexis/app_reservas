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
            'tipo': self.tipo
        }
    @staticmethod
    def get_usertype(user):
        try:
            type_user = TiposUsuario.query.filter_by(id_user_types=user.user_types_id).first()
            return str(type_user.type).replace('UserType.', '')

        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)}), 400
