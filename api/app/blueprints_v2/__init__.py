from flask import Blueprint

api = Blueprint('api_v2', __name__)

from api.app.servicios.v2.routes import servicios_route
from api.app.usuarios.v2.routes import usuarios_route
from api.app.login.v2.routes import login_route
from api.app.reservas.v2.routes import reservas_route
from api.app.preguntas.v2.routes import preguntas_route
from api.app.pagos.v2.routes import pagos_route