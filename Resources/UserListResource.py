from flask import jsonify
from flask_restful import reqparse

from Classes.Model import Model
from data.models.User import User


class UserListResource(Model):
    def __init__(self):
        super().__init__('User')

    def get(self):
        users = self.db.query(self.Model).all()
        return jsonify([item.to_dict() for item in users])

    def post(self):
        self.parser.add_argument('name', required=True, type=str)
        self.parser.add_argument('surname', required=True, type=str)
        self.parser.add_argument('age', required=True, type=int)
        self.parser.add_argument('sex', required=True, type=int)
        self.parser.add_argument('password', required=True, type=str)
        self.parser.add_argument('email', required=True, type=str)
        args = self.parser.parse_args()
        user = User(
            name=args['name'],
            surname=args['surname'],
            age=args['age'],
            sex=args['sex'],
            password=args['password'],
            email=args['email']
        )
        self.db.add(user)
        self.db.commit()
        return jsonify(user.to_dict())
