from Classes.Model import Model
from Data.Models.User import User
from Data.Parsers import user_parser

from sqlalchemy.exc import IntegrityError, OperationalError
from flask import jsonify


class UserListResource(Model):
    def __init__(self):
        super().__init__("User")

    def get(self):
        session = self.db.create_session()
        users = session.query(self.Model).all()
        return jsonify([item.to_dict() for item in users])

    def post(self):
        # TODO: Возможность добавления к пользователю интересов и фотографий
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
        session = self.db.create_session()
        try:
            session.add(user)
            session.commit()
            return jsonify({"message": "User successfully added", "user": user.to_dict()})
        except IntegrityError:
            return jsonify({"Error": "User with such email exists"})
        except OperationalError as ex:
            error_handler = ex.args[0].split("'")[1]
            if error_handler == "check_sex":
                return jsonify({"Error": "User field sex can be only 1 - male or 2 - female"})
