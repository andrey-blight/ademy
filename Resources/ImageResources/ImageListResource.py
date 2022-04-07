from Classes.Model import Model
from Data.Models.Image import Image
from Data.Models.User import User
from Data.Parsers import image_parser
from Data.Functions import token_required

from sqlalchemy.exc import OperationalError
from flask import jsonify
from flask.wrappers import Response
from flask_restful import abort


class ImageListResource(Model):
    def __init__(self):
        super().__init__("Image")

    @token_required
    def get(self, user_id: int) -> Response:
        session = self.db.create_session()
        try:
            if user_id:
                user = session.query(User).get(user_id)
                if user is None:
                    raise IndexError
                images = user.images
            else:
                images = session.query(self.Model).all()
            return jsonify([item.to_dict() for item in images])
        except IndexError:
            abort(404, message=f"User {user_id} not found")
    @token_required
    def post(self, user_id: int) -> Response:
        args = image_parser.parse_args()
        session = self.db.create_session()
        try:
            image = Image(
                user_id=user_id,
                image_href=args["image_href"],
            )
            user = session.query(User).get(user_id)
            if user is None:
                raise IndexError
            user.images.append(image)
            session.commit()
            return jsonify({"message": f"Image successfully added to User {user_id}", "image": image.to_dict()})
        except IndexError:
            session.rollback()
            abort(404, message=f"User {user_id} not found")
        except OperationalError as ex:
            session.rollback()
            error_handler = ex.args[0].split("'")[1]
            if error_handler == "check_count_for_one_user":
                return jsonify({"Error": f"User {user_id} can have maximum 5 images"})
