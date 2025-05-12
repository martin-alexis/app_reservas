from api.app.reservas.models.reservas_model import Reservas
from api.app.servicios.models.servicios_model import Servicios
from api.app.usuarios.models.usuarios_model import Usuarios
from api.app.reservas.schemas.schema_reservas import ReservasSchema
from api.app.servicios.schemas.schema_servicios import ServiciosSchema
from api.app.usuarios.schemas.schema_usuarios import UsuariosSchema
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
