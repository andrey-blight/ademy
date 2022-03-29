from functions import load_environment_variable

from os import environ

from sqlalchemy import create_engine

load_environment_variable()
conn_str = environ.get("DEV_MYSQL_URI")
engine = create_engine(conn_str)
engine.connect()
print(engine)
