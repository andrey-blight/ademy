from Classes.Model import Model
from Data.Models.User import User

from random import choices

from flask import jsonify
from flask.wrappers import Response


class UserRecommendResource(Model):
    def __init__(self):
        super().__init__("User")

    def get(self, count: int, sex: int) -> Response:
        """
        Get the transmitted number of users of the specified gender
        :param count: count of user objects
        :param sex: needed gender
        :return: JSON with users
        """
        try:
            if sex not in [1, 2]:
                return jsonify({"error": "Sex can be only 1 or 2"})
            session = self.db.create_session()
            users = session.query(self.Model).filter(sex == User.sex).all()
            count = min(count, len(users))
            need_users = choices(users, k=count)
            return jsonify({"count": count,
                            "users": [item.to_dict() for item in need_users]})
        except Exception as ex:
            print(ex)
            return jsonify({"error": "Unexpected"})
