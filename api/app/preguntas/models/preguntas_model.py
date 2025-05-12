from datetime import datetime

from api.app import db
from sqlalchemy import DateTime, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


class Preguntas(db.Model):
    __tablename__ = 'preguntas'
    id_preguntas = db.Column(Integer, primary_key=True)
    pregunta = db.Column(String(255), nullable=False)
    respuesta = db.Column(String(255))
    fecha_pregunta = db.Column(DateTime, nullable=False)
    fecha_respuesta = db.Column(DateTime)
    servicios_id = db.Column(Integer, ForeignKey('servicios.id_servicios'), nullable=False)
    usuarios_pregunta_id = db.Column(Integer, ForeignKey('usuarios.id_usuarios'), nullable=False)
    usuarios_respuesta_id = db.Column(Integer, ForeignKey('usuarios.id_usuarios'))

    servicio = relationship('Servicios', back_populates='preguntas')
    usuario_pregunta = relationship('Usuarios', foreign_keys=[usuarios_pregunta_id])
    usuario_respuesta = relationship('Usuarios', foreign_keys=[usuarios_respuesta_id])

    def __init__(self, pregunta, servicios_id, usuarios_pregunta_id, respuesta, fecha_respuesta, usuarios_respuesta_id):
        self.pregunta = pregunta
        self.respuesta = respuesta
        self.fecha_respuesta = datetime.now()
        self.fecha_respuesta = fecha_respuesta
        self.servicios_id = servicios_id
        self.usuarios_pregunta_id = usuarios_pregunta_id
        self.usuarios_respuesta_id = usuarios_respuesta_id
