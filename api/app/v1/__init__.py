from flask import Blueprint

api = Blueprint('api_v1', __name__)

from api.app.v1.routes import auth_route
from api.app.v1.routes import pagos_route
from api.app.v1.routes import reservas_route
from api.app.v1.routes import services_route
from api.app.v1.routes import usuarios_route
from api.app.v1.routes import valoraciones_route


