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
    app.json.sort_keys = False

    from api.app.v1 import api as api_v1
    app.register_blueprint(api_v1, url_prefix='/api/v1.0')

    from api.app.v2 import api as api_v2
    app.register_blueprint(api_v2, url_prefix='/api/v2.0')

    return app
