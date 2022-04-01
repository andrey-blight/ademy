from .functions import load_environment_variable
from os import environ
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker

SqlAlchemyBase = declarative_base()
__session = None


# TODO: Переделать в класс

def global_init():
    global __session
    if __session:  # if session config created do nothing
        return
    load_environment_variable()
    conn_str = environ.get("DEV_MYSQL_URI")  # get connection str from environment variable
    engine = create_engine(conn_str, echo=False)
    __session = sessionmaker(bind=engine, autoflush=False, autocommit=False)  # create session config
    # TODO: автоматически добавлять модели
    from .models import Image, Interests, User
    # SqlAlchemyBase.metadata.drop_all(bind=engine)  # removing data from database
    # SqlAlchemyBase.metadata.create_all(bind=engine)  # adding data to database


def create_session() -> Session:
    global __session
    return __session()  # return Session object from session config
