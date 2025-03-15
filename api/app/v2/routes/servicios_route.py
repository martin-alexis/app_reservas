from api.app.v2 import api_v2 as api
from api.app.utils import common_routes as common

@api.route('/servicios/<int:id_servicio>', methods=['GET'])
def obtener_servicio_id (id_servicio):
       return common.obtener_servicio_por_id(id_servicio)
