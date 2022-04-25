from Classes.Model import Model
from Data.Functions import token_required

from flask import jsonify
from flask.wrappers import Response


class LikeResource(Model):
    def __init__(self):
        super().__init__("User")

    @token_required
    def post(self, from_id: int, to_id: int) -> Response:
        try:
            session = self.db.create_session()
            user_from = session.query(self.Model).get(from_id)
            user_from.set_like(to_id, session=session)
            return jsonify({"Message": f"Set like from user {from_id} to user {to_id}"})
        except Exception as ex:
            return jsonify({"Error": "Unexpected"})
