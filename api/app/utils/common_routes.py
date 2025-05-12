from api.app.models.reservas.reservas_model import Reservas
from api.app.models.services.servicios_model import Servicios
from api.app.models.users.usuarios_model import Usuarios
from api.app.schemas.reservas.schema_reservas import ReservasSchema
from api.app.schemas.servicios.schema_servicios import ServiciosSchema
from api.app.schemas.usuarios.schema_usuarios import UsuariosSchema
from api.app.utils.responses import APIResponse


def obtener_servicio_por_id(id_servicio):
    try:
        servicio = Servicios.query.get(id_servicio)
        if not servicio:
            return APIResponse.not_found(resource='Servicio')
        servicio_schema = ServiciosSchema()
        return APIResponse.success(data=servicio_schema.dump(servicio))
    except Exception as e:
        return APIResponse.error(error= str(e))


def obtener_usuario_por_id(id_usuario):
    try:
        usuario = Usuarios.query.get(id_usuario)
        if not usuario:
            return APIResponse.not_found(resource='Usuario')
        usuario_schema = UsuariosSchema()
        return APIResponse.success(data=usuario_schema.dump(usuario))
    except Exception as e:
        return APIResponse.error(error= str(e))

def obtener_reserva_por_id(id_reserva):
    try:
        reserva = Reservas.query.get(id_reserva)
        if not reserva:
            return APIResponse.not_found(resource='Reserva')
        reserva_schema = ReservasSchema()
        return APIResponse.success(data=reserva_schema.dump(reserva))
    except Exception as e:
        return APIResponse.error(error= str(e))
