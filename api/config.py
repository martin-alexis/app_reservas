import json

from dotenv import load_dotenv
import os

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Configuraciones de Flask y SQLAlchemy
class Config:
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    DATABASE_TOKEN = os.getenv('DATABASE_TOKEN')
    SECRET_KEY = os.getenv('SECRET_KEY')
