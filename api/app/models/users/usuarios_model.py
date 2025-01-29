from werkzeug.security import generate_password_hash, check_password_hash

from api.app import db
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


class Usuarios(db.Model):
    __tablename__ = 'usuarios'
    id_usuarios = db.Column(Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(String(45), nullable=False)
    correo = db.Column(String(45), nullable=False, unique=True)
    contrasena = db.Column(String(255), nullable=False)
    telefono = db.Column(String(45), nullable=False, unique=True)
    tipos_usuario_id = db.Column(Integer, ForeignKey('tipos_usuario.id_tipos_usuario'), nullable=False)

    tipo_usuario = relationship('TiposUsuario', back_populates='usuarios')
    roles = relationship('UsuariosTieneRoles', back_populates='usuario')
    servicios = relationship('Servicios', back_populates='proveedor')
    # reservas = relationship('Reservas', back_populates='usuario')
    # calificaciones = relationship('Calificaciones', back_populates='usuario')

    def __init__(self, nombre, correo, contrasena, telefono, tipos_usuario_id):
        self.nombre = nombre
        self.correo = correo
        self.contrasena = Usuarios.set_password(contrasena)
        self.telefono = telefono
        self.tipos_usuario_id = tipos_usuario_id

    def to_json(self):
        return {
            'id_usuarios': self.id_usuarios,
            'nombre': self.nombre,
            'correo': self.correo,
            'telefono': self.telefono,
            'tipos_usuario_id': self.tipos_usuario_id,
            'tipo_usuario': self.tipo_usuario.to_json() if self.tipo_usuario else None
        }

    @staticmethod
    def set_password(password):
        # Genera un hash de la contraseña y lo guarda
        return generate_password_hash(password)

    def check_password(self, password):
        # Verifica si la contraseña ingresada coincide con el hash guardado
        return check_password_hash(self.contrasena, password)

