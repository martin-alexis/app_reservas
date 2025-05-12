import enum

from api.app import db
from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from sqlalchemy.orm import relationship


class Tipo(enum.Enum):
    GIMNASIOS_Y_ENTRENAMIENTOS = "GIMNASIOS Y ENTRENAMIENTOS"
    ALQUILER_DE_VEHICULOS = "ALQUILER DE VEHICULOS"
    HOTELES_Y_HOSPEDAJES = "HOTELES Y HOSPEDAJES"
    SALONES_DE_EVENTOS = "SALONES DE EVENTOS"
    CINES_Y_TEATROS = "CINES Y TEATROS"
    SPA_Y_MASAJES = "SPA Y MASAJES"
    RESTAURANTES_Y_BARES = "RESTAURANTES Y BARES"
    OTROS = "OTROS"

class TiposServicio(db.Model):
    __tablename__ = 'tipos_servicio'
    id_tipos_servicio = db.Column(Integer, primary_key=True, autoincrement=True)
    # El parámetro values_callable es clave: le dice a SQLAlchemy que use los valores de los enums (e.value) en lugar de sus nombres (e.name)
    tipo = db.Column(Enum(Tipo, values_callable=lambda obj: [e.value for e in obj]), nullable=False)

    servicios = relationship('Servicios', back_populates='tipo_servicio')

    def __init__(self, tipo):
        self.tipo = tipo

    def to_json(self):
        return {
            'id_tipos_servicio': self.id_tipos_servicio,
            'tipo': self.tipo.value
        }
