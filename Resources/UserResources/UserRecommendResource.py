from Classes.Model import Model
from Data.Models.User import User
from Data.Parsers import user_parser
from Data.Functions import token_required
from Data.Models.Interest import Interest
from Data.Models.Image import Image

from sqlalchemy.exc import IntegrityError, OperationalError
from flask import jsonify
from flask.wrappers import Response


class UserRecommendResource(Model):
    def __init__(self):
        super().__init__("User")

    @token_required
    def get(self, count: int) -> Response:
        session = self.db.create_session()
        users = session.query(self.Model).all()
        return jsonify([item.to_dict() for item in users])
