from Classes.Model import Model
from Data.Models.User import User
from Data.Parsers import user_parser
from Data.Functions import token_required
from Data.Models.Interest import Interest
from Data.Models.Image import Image

from sqlalchemy.exc import IntegrityError, OperationalError
from flask import jsonify
from flask.wrappers import Response


class UserListResource(Model):
    def __init__(self):
        super().__init__("User")

    @token_required
    def get(self) -> Response:
        session = self.db.create_session()
        users = session.query(self.Model).all()
        return jsonify([item.to_dict() for item in users])

    # TODO:Разобраться с токеном
    # @token_required
    def post(self) -> Response:
        args = user_parser.parse_args()
        user = User(
            name=args["name"],
            surname=args["surname"],
            age=args["age"],
            about_yourself=args.get("about_yourself", None),
            sex=args["sex"],
            password=args["password"],
            email=args["email"],
        )
        session = self.db.create_session()
        try:
            for interest_name in args["interests"]:
                interest_obj = session.query(Interest).filter(
                    Interest.name == interest_name).first()
                user.interests.append(interest_obj)
            session.add(user)
            session.commit()
            filename = f"{user.id}_1.jpg"
            img = Image(user_id=user.id, image_href=filename)
            user.images.append(img)
            session.commit()
            return jsonify(
                {"message": "User successfully added", "user": user.to_dict()})
        except IntegrityError:
            session.rollback()
            return jsonify({"Error": "User with such email exists"})
        except OperationalError as ex:
            session.rollback()
            error_handler = ex.args[0].split("'")[1]
            if error_handler == "check_sex":
                return jsonify({
                    "Error": "User field sex can "
                             "be only 1 - male or 2 - female"})
