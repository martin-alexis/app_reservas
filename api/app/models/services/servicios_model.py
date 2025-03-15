from api.app import db
from sqlalchemy import Column, Integer, String, ForeignKey, DECIMAL, Boolean, Numeric
from sqlalchemy.orm import relationship


class Servicios(db.Model):
    __tablename__ = 'servicios'
    id_servicios = db.Column(Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(String(45), nullable=False)
    descripcion = db.Column(String(255), nullable=False)
    precio = db.Column(Numeric(10, 0), nullable=False)
    ubicacion = db.Column(String(45), nullable=False)
    imagen = db.Column(String(255))
    tipos_servicio_id = db.Column(Integer, ForeignKey('tipos_servicio.id_tipos_servicio'), nullable=False)
    usuarios_proveedores_id = db.Column(Integer, ForeignKey('usuarios.id_usuarios'), nullable=False)
    disponibilidad_servicio_id = db.Column(Integer, ForeignKey('disponibilidad_servicio.id_disponibilidad_servicio'),
                                           nullable=False)

    tipo_servicio = relationship('TiposServicio', back_populates='servicios')
    proveedor = relationship('Usuarios', back_populates='servicios')

    disponibilidad = relationship('DisponibilidadServicio', back_populates='servicios')
    reservas = relationship('Reservas', back_populates='servicio')
    # valoraciones = relationship('Valoraciones', back_populates='servicio')

    def __init__(self, nombre, descripcion, precio, ubicacion, imagen, tipos_servicio_id, usuarios_proveedores_id, disponibilidad_servicio_id):
        self.nombre = nombre
        self.descripcion = descripcion
        self.precio = precio
        self.ubicacion = ubicacion
        self.imagen = imagen
        self.tipos_servicio_id = tipos_servicio_id
        self.usuarios_proveedores_id = usuarios_proveedores_id
        self.disponibilidad_servicio_id = disponibilidad_servicio_id

    def to_json(self):
        return {
            'id_servicios': self.id_servicios,
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'precio': float(self.precio),
            'ubicacion': self.ubicacion,
            'imagen': self.imagen,
            'tipos_servicio': self.tipo_servicio.to_json() if self.tipo_servicio else None,
            'disponibilidad_servicio': self.disponibilidad.to_json() if self.disponibilidad else None,
            'usuarios_proveedores': self.proveedor.to_json() if self.proveedor else None,


        }