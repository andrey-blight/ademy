from Classes.Model import Model
from Data.Functions import token_required
from Data.Models.User import User
from Data.Parsers import image_edit_parser

from flask import jsonify
from flask.wrappers import Response
from flask_restful import abort
from sqlalchemy.exc import OperationalError


class ImageResource(Model):
    def __init__(self):
        super().__init__("Image")

    @token_required
    def get(self, image_id: int) -> Response:
        session = self.db.create_session()
        image = self.get_object(image_id, session)
        return jsonify(image.to_dict())

    @token_required
    def put(self, image_id: int) -> Response:
        args = image_edit_parser.parse_args()
        session = self.db.create_session()
        image = self.get_object(image_id, session)
        try:
            if args["user_id"] is not None:
                user = session.query(User).get(args["user_id"])
                if user is None:
                    raise IndexError
            for arg in args:
                if args[arg] is not None:
                    setattr(image, arg, args[arg])
            session.commit()
            return jsonify({"message": "Image successfully updated", "image": image.to_dict()})
        except IndexError:
            session.rollback()
            abort(404, message=f"User {args['user_id']} not found")
        except OperationalError as ex:
            session.rollback()
            error_handler = ex.args[0].split("'")[1]
            if error_handler == "check_count_for_one_user":
                return jsonify({"Error": "User with such id can have maximum 5 images"})
        except Exception as ex:
            session.rollback()
            print(ex)
            return jsonify({"Error": "Unexpected"})

    @token_required
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
