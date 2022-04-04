from Data.Functions import load_environment_variable, get_models_path

import importlib
import os
from os import environ

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker

SqlAlchemyBase = declarative_base()
_session = None


class SqlAlchemyDatabase:
    def __init__(self, create=False, delete=False):
        """
        Init database
        :param create: if true create all Models
        :param delete: if true delete all Models
        """
        self._global_init(create, delete)

    @staticmethod
    def _global_init(create: bool, delete: bool) -> None:
        global _session
        if _session:  # if session config created do nothing
            return None
        load_environment_variable()
        conn_str = environ.get("DEV_MYSQL_URI")  # get connection str from environment variable
        engine = create_engine(conn_str, echo=False)
        _session = sessionmaker(bind=engine, autoflush=False, autocommit=False)  # create session config
        abs_path = os.path.abspath(os.curdir)
        os.chdir(get_models_path(abs_path))
        files = [el.split('.')[0] for el in os.listdir() if el.endswith(".py")]  # get all files with Models
        os.chdir(r"../../")
        for module in files:
            importlib.import_module("Data.Models." + module)  # import them in current file
        if delete:
            SqlAlchemyBase.metadata.drop_all(bind=engine)  # removing Data from database
        if create:
            SqlAlchemyBase.metadata.create_all(bind=engine)  # adding Data to database

    @staticmethod
    def create_session() -> Session:
        global _session
        return _session()  # return Session object from session config
