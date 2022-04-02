from Classes.SqlAlchemyDatabase import SqlAlchemyDatabase
from flask_restful import Resource, abort, reqparse
import importlib
import importlib.util, importlib.resources


class Model(Resource):
    def __init__(self, child_class_name: str):
        self.db = SqlAlchemyDatabase()
        self.parser = reqparse.RequestParser()
        self._child_class_name = child_class_name
        # TODO: Убрать зависимость между путем, то есть нужно искать сам файл, а не писать тут его название
        self.Model = getattr(importlib.import_module('data.models.' + child_class_name), child_class_name)

    def is_id_exists(self, id: int) -> None:
        session = self.db.create_session()
        query = session.query(self.Model).get(id)
        if not query:
            abort(404, message=f"{self._child_class_name} model doesn't have the id: {id}")
