from Classes.Model import Model
from Data.Functions import token_required

from flask import jsonify
from flask.wrappers import Response


class UsersChatsResource(Model):
    def __init__(self):
        super().__init__("User")

    @token_required
    def get(self, user_id: int) -> Response:
        try:
            session = self.db.create_session()
            user = session.query(self.Model).get(user_id)
            chats = user.chats
            return jsonify([item.to_dict() for item in chats])
        except Exception as ex:
            print(ex)
            return jsonify({"Error": "Unexpected"})
