from werkzeug.security import generate_password_hash, check_password_hash

from api.app import db
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from api.app.preguntas.models.preguntas_model import Preguntas


class Usuarios(db.Model):
    __tablename__ = 'usuarios'
    id_usuarios = db.Column(Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(String(45), nullable=False)
    correo = db.Column(String(45), nullable=False, unique=True)
    contrasena = db.Column(String(255), nullable=True)
    telefono = db.Column(String(45), nullable=False, unique=True)
    imagen = db.Column(String(255))
    tipos_usuario_id = db.Column(Integer, ForeignKey('tipos_usuario.id_tipos_usuario'), nullable=False)

    tipo_usuario = relationship('TiposUsuario', back_populates='usuarios')
    roles = relationship('UsuariosTieneRoles', back_populates='usuario')
    servicios = relationship('Servicios', back_populates='proveedor')
    pagos = relationship('Pagos', back_populates='usuario')

    preguntas_pregunta = relationship('Preguntas', foreign_keys=[Preguntas.usuarios_pregunta_id],
                                      back_populates='usuario_pregunta')
    preguntas_respuesta = relationship('Preguntas', foreign_keys=[Preguntas.usuarios_respuesta_id],
                                       back_populates='usuario_respuesta')

    # valoraciones = relationship('Valoraciones', back_populates='usuario')

    def __init__(self, nombre, correo, telefono, imagen, tipos_usuario_id, contrasena=None):
        self.nombre = nombre
        self.correo = correo
        self.contrasena = Usuarios.set_password(contrasena) if contrasena else None
        self.telefono = telefono
        self.imagen = imagen
        self.tipos_usuario_id = tipos_usuario_id

    def to_json(self):
        return {
            'id_usuarios': self.id_usuarios,
            'nombre': self.nombre,
            'correo': self.correo,
            'telefono': self.telefono,
            'imagen': self.imagen,
            'tipo_usuario': self.tipo_usuario.to_json() if self.tipo_usuario else None,
            'roles': [relacion.rol.to_json() for relacion in self.roles]

        }

    @staticmethod
    def set_password(password):
        # Genera un hash de la contraseña y lo guarda
        if password is None:
            return None
        return generate_password_hash(password)

    def check_password(self, password):
        # Verifica si la contraseña ingresada coincide con el hash guardado
        if self.contrasena is None:
            return False
        return check_password_hash(self.contrasena, password)

