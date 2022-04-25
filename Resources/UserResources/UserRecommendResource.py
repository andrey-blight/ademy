from Classes.Model import Model
from Data.Models.User import User
from Data.Functions import token_required

from random import choices

from flask import jsonify
from flask_login import current_user
from flask.wrappers import Response


class UserRecommendResource(Model):
    def __init__(self):
        super().__init__("User")

    @token_required
    def get(self, count: int) -> Response:
        try:
            if current_user.is_authenticated:
                session = self.db.create_session()
                users = session.query(self.Model).filter(current_user.sex != User.sex).all()
                need_users = choices(users, k=count)
                return jsonify([item.to_dict() for item in need_users])
        except Exception as ex:
            return jsonify({"Error": "Unexpected"})
