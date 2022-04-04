def load_environment_variable() -> None:
    """This function loads environment variable from .env file"""
    from os import path
    from dotenv import load_dotenv  # library for work with .env files
    basedir = path.abspath(path.dirname(__file__))  # find absolute path
    load_dotenv(path.join(basedir, r"../.env"))  # add .env to path and load .env file


def get_models_path(abs_path: str) -> str:
    """Get path for import Models"""
    elements = abs_path.split("\\")
    if len(elements) < 2 or elements[-2] != "Data":
        elements.extend(("Data", "Models"))
    elif elements[-1] != "Models":
        elements.append("Models")
    return '\\'.join(el for el in elements)
