def load_environment_variable():
    """This function loads environment variable from .env file"""
    from os import path
    from dotenv import load_dotenv  # library for work with .env files
    basedir = path.abspath(path.dirname(__file__))  # find absolute path
    load_dotenv(path.join(basedir, '../.env'))  # add .env to path and load .env file