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


    from .routes.usuarios_route import user_bp
    app.register_blueprint(user_bp, url_prefix='/')

    from .routes.auth_route import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/')

    from .routes.services_route import services_bp
    app.register_blueprint(services_bp, url_prefix='/')

    from .routes.reservas_route import reservas_bp
    app.register_blueprint(reservas_bp, url_prefix='/')

    from .routes.valoraciones_route import valoraciones_bp
    app.register_blueprint(valoraciones_bp, url_prefix='/')

    from .routes.pagos_route import pagos_bp
    app.register_blueprint(pagos_bp, url_prefix='/')

    return app
