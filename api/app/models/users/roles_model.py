import enum

from flask import jsonify

from api.app import db
from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.orm import relationship

from api.app.models.users.usuarios_tiene_roles_model import UsuariosTieneRoles


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
    @staticmethod
    def get_roles_user(user):
        try:
            roles_user = []
            user_role_relations = UsuariosTieneRoles.query.filter_by(usuarios_id=user.id_usuarios).all()

            for relation in user_role_relations:
                role = Roles.query.get(relation.roles_id)
                if role:
                    role_str = str(role.tipo).replace('TipoRoles.', '')
                    roles_user.append(role_str)
            return roles_user
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)}), 400
