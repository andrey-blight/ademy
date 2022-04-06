from Data.Functions import load_environment_variable

from os import environ

load_environment_variable()


class Config:
    SECRET_KEY = environ.get("SECRET_KEY")
    UPLOAD_FOLDER = r"static/user_images"
    STATIC_FOLDER = "static"
    TEMPLATES_FOLDER = "templates"


class DevConfig(Config):
    FLASK_ENV = "development"
    DEBUG = True
    TESTING = True
