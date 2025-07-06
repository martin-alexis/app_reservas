from dotenv import load_dotenv
import os
import logging
from logging.handlers import RotatingFileHandler
from sqlalchemy import create_engine
import datetime

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True  # Activar el pre-ping en el pool de conexiones
    }
    SECRET_KEY = os.getenv('SECRET_KEY')
    TOKEN_SECRET = os.getenv('TOKEN_SECRET')
    CLIENT_ID = os.getenv('CLIENT_ID')
    CLIENT_SECRET = os.getenv('CLIENT_SECRET')

    @staticmethod
    def select_config(app):
        env = os.getenv("FLASK_ENV", "development")

        if env == "testing":
            app.config.from_object("api.config.TestConfig")
        elif env == "production":
            app.config.from_object("api.config.ProductionConfig")
        elif env == "development":
            app.config.from_object("api.config.DevelopmentConfig")

        return app


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = (
        f"sqlite+{os.environ.get('TURSO_DATABASE_DEVELOPMENT_URI')}?secure=true&check_same_thread=false"
    )
    SQLALCHEMY_ENGINE_OPTIONS = {
        "connect_args": {
            "auth_token": os.environ.get('TURSO_DATABASE_DEVELOPMENT_TOKEN')
        }
    }

    SQLALCHEMY_TRACK_MODIFICATIONS = False  


class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False

    SQLALCHEMY_DATABASE_URI = (
        f"sqlite+{os.environ.get('TURSO_DATABASE_PRODUCTION_URI')}?secure=true&check_same_thread=false"
    )
    SQLALCHEMY_ENGINE_OPTIONS = {
        "connect_args": {
            "auth_token": os.environ.get('TURSO_DATABASE_PRODUCTION_TOKEN')
        }
    }
    LOGGING_LEVEL = "ERROR"  # Solo registrar errores o más graves

    # Configuración básica del logging
    logging.basicConfig(
        level=logging.DEBUG,  # Establece el nivel global de logging para capturar todos los logs
        format="%(asctime)s - %(levelname)s - %(message)s",  # Formato del log
        handlers=[
            logging.StreamHandler(),  # Mostrar los logs en la consola
            RotatingFileHandler('app_production.log', maxBytes=10000000, backupCount=5)  # Guardar logs en archivo
        ]
    )

    # Establecer el nivel de logging global
    logging.getLogger().setLevel(logging.ERROR)  # Solo se registrarán errores o más graves en producción

class TestConfig(Config):
    TESTING = True
    basedir = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(basedir, 'test.db')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True


