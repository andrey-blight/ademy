from Classes.Model import Model

from flask import jsonify
from flask.wrappers import Response


class InterestListResource(Model):
    def __init__(self):
        super().__init__("Interest")

    def get(self) -> Response:
        """
        Get all interests from database
        :return: list of interests in JSON
        """
        session = self.db.create_session()
        interests = session.query(self.Model).all()
        return jsonify({"names": [item.to_dict()["name"] for item in interests]})
