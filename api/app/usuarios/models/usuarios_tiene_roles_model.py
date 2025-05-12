from api.app import db
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship


class UsuariosTieneRoles(db.Model):
    __tablename__ = 'usuarios_tiene_roles'
    id_usuarios_tiene_roles = db.Column(Integer, primary_key=True, autoincrement=True)
    usuarios_id = db.Column(Integer, ForeignKey('usuarios.id_usuarios'), nullable=False)
    roles_id = db.Column(Integer, ForeignKey('roles.id_roles'), nullable=False)

    usuario = relationship('Usuarios', back_populates='roles')
    rol = relationship('Roles', back_populates='usuarios')

    def __init__(self, usuarios_id, roles_id):
        self.usuarios_id = usuarios_id
        self.roles_id = roles_id

    def to_json(self):
        return {
            'id_usuarios_tiene_roles': self.id_usuarios_tiene_roles,
            'usuarios_id': self.usuarios_id,
            'roles_id': self.roles_id,
            'rol': self.rol.to_json() if self.rol else None
        }