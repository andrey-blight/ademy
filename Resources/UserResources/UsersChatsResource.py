from Classes.Model import Model

from flask import jsonify
from flask.wrappers import Response


class UsersChatsResource(Model):
    def __init__(self):
        super().__init__("User")

    def get(self, user_id: int) -> Response:
        """
        Get all users chats ordered by create time (first are newest)
        :param user_id: id of user
        :return: list of chats
        """
        session = self.db.create_session()
        user = self.get_object(user_id, session)
        try:
            chats = sorted(user.chats, key=lambda el: el.last_message.created_at, reverse=True)
            print(chats)
            return jsonify([item.to_dict() for item in chats])
        except Exception as ex:
            print(ex)
            return jsonify({"Error": "Unexpected"})
