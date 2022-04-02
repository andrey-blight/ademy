def load_environment_variable():
    """This function loads environment variable from .env file"""
    from os import path
    from dotenv import load_dotenv  # library for work with .env files
    basedir = path.abspath(path.dirname(__file__))  # find absolute path
    load_dotenv(path.join(basedir, r"../.env"))  # add .env to path and load .env file


def get_models_path(abs_path):
    elements = abs_path.split("\\")
    if len(elements) < 2 or elements[-2] != "data":
        elements.extend(("data", "models"))
    elif elements[-1] != "models":
        elements.append("models")
    return '\\'.join(el for el in elements)
