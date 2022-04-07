from Classes.Model import Model
from Data.Models.Interest import Interest
from Data.Models.User import User
from Data.Parsers import interest_parser
from Data.Functions import token_required

from flask import jsonify
from flask.wrappers import Response
from flask_restful import abort


class InterestListResource(Model):
    def __init__(self):
        super().__init__("Interest")

    @token_required
    def get(self, user_id: int) -> Response:
        session = self.db.create_session()
        try:
            if user_id:
                user = session.query(User).get(user_id)
                if user is None:
                    raise IndexError
                interests = user.interests
            else:
                interests = session.query(self.Model).all()
            return jsonify([item.to_dict() for item in interests])
        except IndexError:
            abort(404, message=f"User {user_id} not found")

    @token_required
    def post(self, user_id: int) -> Response:
        args = interest_parser.parse_args()
        session = self.db.create_session()
        try:
            interest = Interest(
                name=args["name"],
            )
            user = session.query(User).get(user_id)
            if user is None:
                raise IndexError
            user.interests.append(interest)
            session.commit()
            return jsonify(
                {"message": f"Interest successfully added to User {user_id}", "interest": interest.to_dict()})
        except IndexError:
            session.rollback()
            abort(404, message=f"User {user_id} not found")
