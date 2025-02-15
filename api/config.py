from dotenv import load_dotenv
import os


# Cargar las variables de entorno desde el archivo .env
load_dotenv()

class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY')

    @staticmethod
    def select_config(app):
        env = os.getenv("FLASK_ENV", "development")

        if env == "testing":
            app.config.from_object("api.config.TestConfig")
        elif env == "production":
            app.config.from_object("api.config.ProductionConfig")
        else:
            app.config.from_object("api.config.DevelopmentConfig")

        return app


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = f"sqlite+{os.getenv('TURSO_DATABASE_URI')}/?authToken={os.getenv('TURSO_DATABASE_TOKEN')}&secure=true"
    SECRET_KEY = os.getenv('SECRET_KEY')

class ProductionConfig(Config):
    pass

class TestConfig(Config):
    TESTING = True
    basedir = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(basedir, 'test.db')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True


