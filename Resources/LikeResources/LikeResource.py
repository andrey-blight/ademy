from Classes.Model import Model
from Data.Models.Chat import Chat
from Data.Functions import token_required

from flask import jsonify
from flask.wrappers import Response


class LikeResource(Model):
    def __init__(self):
        super().__init__("User")

    @token_required
    def post(self, from_id: int, to_id: int) -> Response:
        session = self.db.create_session()
        try:
            user_from = session.query(self.Model).get(from_id)
            user_to = session.query(self.Model).get(to_id)
            user_from.set_like(to_id, session=session)
            # if the user to whom the like is intended has already liked the
            # current user we create chat between them
            ans = {"Message": f"Set like from user {from_id} to user {to_id}."}
            if user_to in user_from.liked_from:
                chat = Chat()
                chat.users.extend([user_to, user_from])
                ans["Message"] += " Chat between them was created."
                session.add(chat)
            session.commit()
            return jsonify(ans)
        except Exception as ex:
            session.rollback()
            print(ex)
            return jsonify({"Error": "Unexpected"})
