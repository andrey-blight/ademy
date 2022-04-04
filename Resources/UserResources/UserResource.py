from Classes.Model import Model
from Data.Parsers import user_parser

from flask import jsonify


class UserResource(Model):
    def __init__(self):
        super().__init__("User")

    def get(self, user_id: int):
        user = self.get_object(user_id)
        return jsonify(user.to_dict())

    def put(self, user_id: int):
        args = user_parser.parse_args()
        user = self.get_object(user_id)
        session = self.db.create_session()
        try:
            for arg in args:
                if args[arg] is not None:
                    setattr(user, arg, args[arg])
            session.commit()
        except Exception as ex:
            print(ex)
            session.rollback()
        return jsonify(user.to_dict())

    def delete(self, user_id: int):
        session = self.db.create_session()
        user = self.get_object(user_id, close=True)
        try:
            session.delete(user)
            session.commit()
            return jsonify({"message": "User successfully deleted", "user": user.to_dict()})
        except Exception as ex:
            print(type(ex), ex, sep='\n')
            return jsonify({"Error": "Unexpected"})
