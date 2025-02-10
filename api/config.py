from dotenv import load_dotenv
import os


# Cargar las variables de entorno desde el archivo .env
load_dotenv()

class Config:
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = f"sqlite+{os.getenv('TURSO_DATABASE_URI')}/?authToken={os.getenv('TURSO_DATABASE_TOKEN')}&secure=true"
    SECRET_KEY = os.getenv('SECRET_KEY')
