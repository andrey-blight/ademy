from Classes.SqlAlchemyDatabase import SqlAlchemyDatabase

import importlib

from flask_restful import Resource, abort, reqparse


class Model(Resource):
    def __init__(self, child_class_name: str):
        self.db = SqlAlchemyDatabase()
        self.session = self.db.create_session()
        self.parser = reqparse.RequestParser()
        self._child_class_name = child_class_name
        self.Model = getattr(importlib.import_module("data.models." + child_class_name), child_class_name)

    def is_id_exists(self, id: int) -> None:
        try:
            query = self.session.query(self.Model).get(id)
        except BaseException:
            self.session.rollback()
