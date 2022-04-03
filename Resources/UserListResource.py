from flask_restful import abort

from Classes.Model import Model
from data.models.User import User
from data.parsers import user_parser
from Classes.SqlAlchemyDatabase import SqlAlchemyDatabase
from flask import jsonify


class UserListResource(Model):
    def __init__(self):
        super().__init__("User")

    def get(self):
        session = self.db.create_session()
        users = session.query(self.Model).all()
        return jsonify([item.to_dict() for item in users])

    def post(self):
        args = user_parser.parse_args()
        user = User(
            name=args["name"],
            surname=args["surname"],
            age=args["age"],
            about_yourself=args.get("about_yourself", None),
            sex=args["sex"],
            password=args["password"],
            email=args["email"]
        )
        self.db.add(user)
        self.db.commit()
        return jsonify(user.to_dict())
