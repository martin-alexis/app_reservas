from flask import Flask, jsonify, render_template
from flask_cors import CORS
from sqlalchemy.exc import SQLAlchemyError

from api.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from api.oauth import oauth

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
    oauth.init_app(app)
    app.json.sort_keys = False

    from api.app.blueprints_v1 import api as api_v1
    app.register_blueprint(api_v1, url_prefix='/api/v1.0')

    from api.app.blueprints_v2 import api as api_v2
    app.register_blueprint(api_v2, url_prefix='/api/v2.0')

    from api.app.swagger.routes import swagger_bp
    app.register_blueprint(swagger_bp)

    # Inicializar documentación Swagger de forma modular
    from api.app.swagger.apispec_config import initialize_all_documentation
    initialize_all_documentation()

    register_error_handlers(app)
    return app


def register_error_handlers(app):
    @app.errorhandler(SQLAlchemyError)
    def handle_sqlalchemy_error(error):
        app.logger.error(f"Database error: {str(error)}")
        return jsonify({
            "error": "Database error",
            "message": "A problem occurred while accessing the database."
        }), 500

