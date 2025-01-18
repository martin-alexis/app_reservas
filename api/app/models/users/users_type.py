import enum

from flask import jsonify

from api.app import db
from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.orm import relationship

class UserType(enum.Enum):
    PARTICULAR = "PARTICULAR"
    EMPRESA = "EMPRESA"

class UserTypes(db.Model):
    __tablename__ = 'user_types'

    id_user_types = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(Enum(UserType), nullable=False)

    users = relationship('Users', back_populates='user_type')

    def to_dict(self):
        return {
            'id_user_types': self.id_user_types,
            'type': self.type
        }

    @staticmethod
    def get_usertype(user):
        try:
            type_user = UserTypes.query.filter_by(id_user_types=user.user_types_id).first()
            return str(type_user.type).replace('UserType.', '')

        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)}), 400
