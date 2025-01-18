from api.app import db
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship



class UsersHasRoles(db.Model):
    __tablename__ = 'users_has_roles'

    id_users_has_roles = Column(Integer, primary_key=True, autoincrement=True)
    users_id = Column(Integer, ForeignKey('users.id_users'), nullable=False)
    roles_id = Column(Integer, ForeignKey('roles.id_roles'), nullable=False)

    user = relationship('Users', back_populates='users_roles')
    role = relationship('Roles', back_populates='users_roles')

    def to_dict(self):
        return {
            'id_users_has_roles': self.id_users_has_roles,
            'users_id': self.users_id,
            'roles_id': self.roles_id
        }
