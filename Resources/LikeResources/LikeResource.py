from Classes.Model import Model
from Data.Models.Chat import Chat

from flask import jsonify
from flask.wrappers import Response


class LikeResource(Model):
    def __init__(self):
        super().__init__("User")

    def post(self, from_id: int, to_id: int) -> Response:
        """
        This request set like from user with id "from_id" to user with id "to_id"
        If user from have been liked by user_to we create chat between them
        :param from_id: id of the user who likes
        :param to_id: id of the user who is being liked
        :return: JSON response with status of request
        """
        session = self.db.create_session()
        user_from = self.get_object(from_id, session)
        user_to = self.get_object(to_id, session)
        try:
            if user_to in user_from.liked_to:
                return jsonify({"message": f"like from user {from_id} to user {to_id} has been already set"})
            user_from.set_like(to_id, session=session)
            ans = {"message": f"set like from user {from_id} to user {to_id}."}
            if user_to in user_from.liked_from:  # if it's mutual like we create chat between them
                chat = Chat()
                chat.users.extend([user_to, user_from])
                ans["message"] += " Chat between them was created."
                session.add(chat)
            session.commit()
            return jsonify(ans)
        except Exception as ex:
            session.rollback()
            print(type(ex))
            return jsonify({"error": "Unexpected"})
