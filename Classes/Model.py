from Classes.SqlAlchemyDatabase import SqlAlchemyDatabase

import importlib

from flask_restful import Resource, abort


class Model(Resource):
    def __init__(self, child_class_name: str):
        self.db = SqlAlchemyDatabase()
        self._child_class_name = child_class_name
        self.Model = getattr(importlib.import_module("Data.Models." + child_class_name), child_class_name)

    # TODO: подумать что с этим сделать
    def get_object(self, id: int):
        """
        :param id:
        :return: self.Model object
        """
        session = self.db.create_session()
        try:
            obj = session.query(self.Model).get(id)
            return obj
        except Exception as ex:
            print(ex)
            abort(404, message=f"{self._child_class_name} {id} not found")
