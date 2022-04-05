from Classes.Model import Model
from Data.Models.Image import Image
from Data.Parsers import image_parser

from sqlalchemy.exc import OperationalError
from flask import jsonify
from flask.wrappers import Response


class UserListResource(Model):
    def __init__(self):
        super().__init__("Image")

    def get(self) -> Response:
        session = self.db.create_session()
        image = session.query(self.Model).all()
        return jsonify([item.to_dict() for item in image])

    def post(self) -> Response:
        # TODO: подумать как будут передаваться картинки
        args = image_parser.parse_args()
        image = Image(
            user_id=args["user_id"],
            image=args["image"],
        )
        session = self.db.create_session()
        try:
            session.add(image)
            session.commit()
            return jsonify({"message": "Image successfully added", "image": image.to_dict()})
        except OperationalError as ex:
            session.rollback()
            error_handler = ex.args[0].split("'")[1]
            if error_handler == "check_count_for_one_user":
                return jsonify({"Error": "User with such id can have maximum 5 images"})
