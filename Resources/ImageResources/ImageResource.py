from Classes.Model import Model
from Data.Parsers import image_edit_parser

from flask import jsonify
from flask.wrappers import Response
from sqlalchemy.exc import OperationalError


class UserResource(Model):
    def __init__(self):
        super().__init__("User")

    def get(self, image_id: int) -> Response:
        session = self.db.create_session()
        image = self.get_object(image_id, session)
        return jsonify(image.to_dict())

    def put(self, image_id: int) -> Response:
        args = image_edit_parser.parse_args()
        session = self.db.create_session()
        image = self.get_object(image_id, session)
        try:
            for arg in args:
                if args[arg] is not None:
                    setattr(image, arg, args[arg])
            session.commit()
            return jsonify({"message": "Image successfully updated", "image": image.to_dict()})
        except OperationalError as ex:
            session.rollback()
            error_handler = ex.args[0].split("'")[1]
            if error_handler == "check_count_for_one_user":
                return jsonify({"Error": "User with such id can have maximum 5 images"})
        except Exception as ex:
            session.rollback()
            print(ex)
            return jsonify({"Error": "Unexpected"})

    def delete(self, image_id: int) -> Response:
        session = self.db.create_session()
        image = self.get_object(image_id, session)
        try:
            session.delete(image)
            session.commit()
            return jsonify({"message": "Image successfully deleted", "image": image.to_dict()})
        except Exception as ex:
            print(type(ex), ex, sep='\n')
            return jsonify({"Error": "Unexpected"})
