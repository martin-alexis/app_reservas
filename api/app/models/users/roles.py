import enum

from flask import jsonify

from api.app import db
from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.orm import relationship

from api.app.models.users.users_has_roles import UsersHasRoles


class RolesType(enum.Enum):
    ADMIN = "ADMIN"
    CLIENTE = "CLIENTE"
    PROVEEDOR = "PROVEEDOR"

class Roles(db.Model):
    __tablename__ = 'roles'

    id_roles = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(Enum(RolesType), nullable=False, unique=True)
    users_roles = relationship('UsersHasRoles', back_populates='role')

    def to_dict(self):
        return {
            'id_roles': self.id_roles,
            'type': self.type.value
        }

    @staticmethod
    def get_roles_user(user):
        try:
            roles_user = []
            user_role_relations = UsersHasRoles.query.filter_by(users_id=user.id_users).all()

            for relation in user_role_relations:
                role = Roles.query.get(relation.roles_id)
                if role:
                    role_str = str(role.type).replace('RolesType.', '')
                    roles_user.append(role_str)
            return roles_user
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)}), 400
