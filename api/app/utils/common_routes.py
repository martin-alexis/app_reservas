
from api.app.models.services.servicios_model import Servicios
from api.app.schemas.servicios.schema_servicios import ServiciosSchema
from api.app.utils.responses import APIResponse


def obtener_servicio_por_id(id_servicio):
    try:
        servicio = Servicios.query.get(id_servicio)
        if not servicio:
            return APIResponse.not_found()
        servicio_schema = ServiciosSchema()
        return APIResponse.success(data=servicio_schema.dump(servicio))
    except Exception as e:
        return APIResponse.error(error= str(e))
