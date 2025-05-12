from datetime import datetime

from api.app import db
from sqlalchemy import DateTime, Integer, String, ForeignKey
from sqlalchemy.orm import relationship



class Valoraciones(db.Model):
    __tablename__ = 'valoraciones'
    id_valoraciones = db.Column(Integer, primary_key=True)
    puntuacion = db.Column(Integer, nullable=False)
    comentario = db.Column(String(45), nullable=False)
    fecha_creacion = db.Column(DateTime, nullable=False)
    servicios_id = db.Column(Integer, ForeignKey('servicios.id_servicios'), nullable=False)
    usuarios_id = db.Column(Integer, ForeignKey('usuarios.id_usuarios'), nullable=False)

    # servicio = relationship('Servicios', back_populates='valoraciones')
    # usuario = relationship('Usuarios', back_populates='valoraciones')
    #

    def __init__(self, puntuacion, comentario, servicios_id, usuarios_id):
        self.puntuacion = puntuacion
        self.comentario = comentario
        self.fecha_creacion = datetime.now()
        self.servicios_id = servicios_id
        self.usuarios_id = usuarios_id

    def to_json(self):
        return {
            'id_valoraciones': self.id_valoraciones,
            'puntuacion': self.puntuacion,
            'comentario': self.comentario,
            'fecha_creacion': self.fecha_creacion.isoformat(),
            'servicios_id': self.servicios_id,
            'usuarios_id': self.usuarios_id,
            'servicio': self.servicio.to_json() if self.servicio else None,
            'usuario': self.usuario.to_json() if self.usuario else None
        }