from Classes.Model import Model
from Data.Parsers import user_parser

from flask import jsonify


class UserResource(Model):
    def __init__(self):
        super().__init__("User")

    def get(self, user_id: int):
        user = self.get_object(user_id)
        if user:
            return jsonify({user.to_dict()})
        else:
            return jsonify({"message": "Error"})

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
        user = session.query(self.Model).delete(user_id)
        session.commit()
        return jsonify(user.to_dict())
