from flask import Flask
from flask_cors import CORS
from api.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
ma = Marshmallow()

def create_app():
    app = Flask(__name__,
                template_folder='../../pages',
                static_folder='../../static')

    CORS(app)

    Config.select_config(app)
    db.init_app(app)
    ma.init_app(app)


    # from api.app.v1.routes.usuarios_route import user_bp
    # app.register_blueprint(user_bp, url_prefix='/')
    #
    # from api.app.v1.routes.auth_route import auth_bp
    # app.register_blueprint(auth_bp, url_prefix='/')
    #
    # from api.app.v1.routes import services_bp
    # app.register_blueprint(services_bp, url_prefix='/')
    #
    # from api.app.v1.routes import reservas_bp
    # app.register_blueprint(reservas_bp, url_prefix='/')
    #
    # from api.app.v1.routes import valoraciones_bp
    # app.register_blueprint(valoraciones_bp, url_prefix='/')
    #
    # from api.app.v1.routes import pagos_bp
    # app.register_blueprint(pagos_bp, url_prefix='/')

    # from api.v1_1 import api as api_v1_1
    # from api.v2 import api as api_v2
    from api.app.v1 import api as api_v1
    app.register_blueprint(api_v1, url_prefix='/api/v1.0')

    # app.register_blueprint(api_v1_1, url_prefix='/v1.1')
    # app.register_blueprint(api_v2, url_prefix='/v2')
    return app
