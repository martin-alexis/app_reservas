
from api.app.models.services.servicios_model import Servicios
from api.app.schemas.servicios.schema_servicios import servicio_schema
from api.app.utils.responses import APIResponse


def obtener_servicio_por_id(id_servicio):
    try:
        servicio = Servicios.query.get(id_servicio)
        if not servicio:
            return APIResponse.not_found(None,'Servicios')
        return APIResponse.success(servicio_schema.dump(servicio), 'Servicio encontrado')
    except Exception as e:
        return APIResponse.error(None, str(e))
