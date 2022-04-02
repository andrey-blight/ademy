from data.functions import load_environment_variable

from os import environ

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.orm.decl_api import DeclarativeMeta


class SqlAlchemyDatabase:
    SqlAlchemyBase = declarative_base()
    __session = None

    def __init__(self, create=False, delete=False):
        """
        Init database
        :param create: if true create all models
        :param delete: if true delete all models
        """
        self._global_init(create, delete)

    def _global_init(self, create: bool, delete: bool) -> None:
        if self.__session:  # if session config created do nothing
            return None
        load_environment_variable()
        conn_str = environ.get("DEV_MYSQL_URI")  # get connection str from environment variable
        engine = create_engine(conn_str, echo=False)
        self.__session = sessionmaker(bind=engine, autoflush=False, autocommit=False)  # create session config
        # TODO: автоматически добавлять модели
        # from data.models import Image, Interests, User
        if delete:
            self.SqlAlchemyBase.metadata.drop_all(bind=engine)  # removing data from database
        if create:
            self.SqlAlchemyBase.metadata.create_all(bind=engine)  # adding data to database

    def get_base(self) -> DeclarativeMeta:
        """
        Get object for inheritance classes
        :return: DeclarativeMeta
        """
        return self.SqlAlchemyBase

    def create_session(self) -> Session:
        return self.__session()  # return Session object from session config
