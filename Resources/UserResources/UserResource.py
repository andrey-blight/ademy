from Classes.Model import Model
from Data.Parsers import user_edit_parser

from flask import jsonify
from flask.wrappers import Response
from sqlalchemy.exc import OperationalError


class UserResource(Model):
    def __init__(self):
        super().__init__("User")

    def get(self, user_id: int) -> Response:
        session = self.db.create_session()
        user = self.get_object(user_id, session)
        return jsonify(user.to_dict())

    def put(self, user_id: int) -> Response:
        args = user_edit_parser.parse_args()
        session = self.db.create_session()
        user = self.get_object(user_id, session)
        try:
            for arg in args:
                if args[arg] is not None:
                    setattr(user, arg, args[arg])
            session.commit()
            return jsonify({"message": "User successfully updated", "user": user.to_dict()})
        except OperationalError as ex:
            session.rollback()
            error_handler = ex.args[0].split("'")[1]
            if error_handler == "check_sex":
                return jsonify({"Error": "User field sex can be only 1 - male or 2 - female"})
        except Exception as ex:
            session.rollback()
            print(ex)
            return jsonify({"Error": "Unexpected"})

    def delete(self, user_id: int) -> Response:
        session = self.db.create_session()
        user = self.get_object(user_id, session)
        try:
            session.delete(user)
            session.commit()
            return jsonify({"message": "User successfully deleted", "user": user.to_dict()})
        except Exception as ex:
            print(type(ex), ex, sep='\n')
            return jsonify({"Error": "Unexpected"})
