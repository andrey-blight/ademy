from os import environ, path
from dotenv import load_dotenv  # library for work with .env files

# we will load secret information from .env file using dotenv and get as environment variable
basedir = path.abspath(path.dirname(__file__))  # find absolute path
load_dotenv(path.join(basedir, '.env'))  # add .env to path and load .env file


class Config:
    SECRET_KEY = environ.get('SECRET_KEY')
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'


class DevConfig(Config):
    FLASK_ENV = 'development'
    DEBUG = True
    TESTING = True
