from Classes.Model import Model
from Data.Functions import token_required

from flask import jsonify
from flask.wrappers import Response


class InterestListResource(Model):
    def __init__(self):
        super().__init__("Interest")

    @token_required
    def get(self) -> Response:
        session = self.db.create_session()
        interests = session.query(self.Model).all()
        return jsonify([item.to_dict() for item in interests])
