from flask import Blueprint

api = Blueprint('api_v2', __name__)
from api.app.v2.routes import servicios_route
