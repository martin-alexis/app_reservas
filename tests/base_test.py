import unittest
from api.app import create_app
from api.app import db
from api.app.usuarios.models.tipos_usuarios_model import TiposUsuario, Tipo as TipoUsuarios
from api.app.usuarios.models.roles_model import Roles, TipoRoles
from api.app.servicios.models.disponibilidad_servicios_model import DisponibilidadServicio, Estado
from api.app.servicios.models.tipos_servicios_model import TiposServicio, Tipo as TipoServicios
from api.app.reservas.models.estados_reserva_model import EstadoReserva, EstadosReserva
from api.app.pagos.models.estados_pago_model import EstadosPago, TiposEstadoPago


class BaseTestCase(unittest.TestCase):
    def setUp(self):
        """ Se ejecuta antes de cada prueba """
        self.app = create_app()
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()  # Crea las tablas en la base de datos en memoria

        # Insertar datos obligatorios en la base de datos
        self.insertar_datos_base(TipoUsuarios, TiposUsuario, db.session, 'tipo')
        self.insertar_datos_base(TipoRoles, Roles, db.session, 'tipo')
        self.insertar_datos_base(TipoServicios, TiposServicio, db.session, 'tipo')
        self.insertar_datos_base(Estado, DisponibilidadServicio, db.session, 'estado')
        self.insertar_datos_base(EstadoReserva, EstadosReserva, db.session, 'estado')
        self.insertar_datos_base(TiposEstadoPago, EstadosPago, db.session, 'estado')


    def insertar_datos_base(self, clase_enum, modelo, db_session, campo):
        for enum in clase_enum:
            # Verifica si ya existe en la base de datos
            if not modelo.query.filter_by(**{campo: enum.name}).first():
                # Crea una nueva instancia del modelo y agrega el valor del Enum
                instancia_modelo = modelo(**{campo: enum.value})
                db_session.add(instancia_modelo)
        db_session.commit()

    def tearDown(self):
        """ Se ejecuta después de cada prueba """
        db.session.remove()
        # db.drop_all()  # Borra todas las tablas
        self.app_context.pop()
