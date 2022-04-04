from Classes.Model import Model
from Data.Parsers import user_edit_parser

from flask import jsonify


class UserResource(Model):
    def __init__(self):
        super().__init__("User")

    def get(self, user_id: int):
        session = self.db.create_session()
        user = self.get_object(user_id, session)
        return jsonify(user.to_dict())

    def put(self, user_id: int):
        args = user_edit_parser.parse_args()
        session = self.db.create_session()
        user = self.get_object(user_id, session)
        try:
            for arg in args:
                if args[arg] is not None:
                    setattr(user, arg, args[arg])
            session.commit()
            return jsonify({"message": "User successfully updated", "user": user.to_dict()})
        except Exception as ex:
            print(ex)
            session.rollback()
            return jsonify({"Error": "Unexpected"})

    def delete(self, user_id: int):
        session = self.db.create_session()
        user = self.get_object(user_id, session)
        try:
            session.delete(user)
            session.commit()
            return jsonify({"message": "User successfully deleted", "user": user.to_dict()})
        except Exception as ex:
            print(type(ex), ex, sep='\n')
            return jsonify({"Error": "Unexpected"})
