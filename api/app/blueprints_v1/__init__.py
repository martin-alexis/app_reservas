from flask import Blueprint

api = Blueprint('api_v1', __name__)

from api.app.login.v1.routes import auth_route
from api.app.pagos.v1.routes import pagos_route
from api.app.reservas.v1.routes import reservas_route
from api.app.servicios.v1.routes import services_route
from api.app.usuarios.v1.routes import usuarios_route



