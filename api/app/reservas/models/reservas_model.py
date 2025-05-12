from datetime import datetime

from api.app import db
from sqlalchemy import Integer, ForeignKey, Numeric, DateTime
from sqlalchemy.orm import relationship

class Reservas(db.Model):
    __tablename__ = 'reservas'
    id_reservas = db.Column(Integer, primary_key=True, autoincrement=True)
    fecha_creacion_reserva = db.Column(DateTime, default=datetime.utcnow, nullable=False)
    fecha_inicio_reserva = db.Column(DateTime, nullable=False)
    fecha_fin_reserva = db.Column(DateTime, nullable=False)
    servicios_id = db.Column(Integer, ForeignKey('servicios.id_servicios'), nullable=False)
    estados_reserva_id = db.Column(Integer, ForeignKey('estados_reserva.id_estados_reserva'), nullable=False)

    servicio = relationship('Servicios', back_populates='reservas')
    estado_reserva = relationship('EstadosReserva', back_populates='reservas')
    pagos = relationship('Pagos', back_populates='reserva')

    def __init__(self, fecha_inicio_reserva, fecha_fin_reserva, servicios_id,
                 estados_reserva_id):
        self.fecha_creacion_reserva = datetime.now()
        self.fecha_inicio_reserva = fecha_inicio_reserva
        self.fecha_fin_reserva = fecha_fin_reserva
        self.servicios_id = servicios_id
        self.estados_reserva_id = estados_reserva_id

