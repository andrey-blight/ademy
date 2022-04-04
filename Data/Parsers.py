from flask_restful import reqparse

user_parser = reqparse.RequestParser()
user_parser.add_argument("name", required=True, type=str)
user_parser.add_argument("surname", required=True, type=str)
user_parser.add_argument("age", required=True, type=int)
user_parser.add_argument("about_yourself", required=False, type=str)
user_parser.add_argument("sex", required=True, type=int)
user_parser.add_argument("password", required=True, type=str)
user_parser.add_argument("email", required=True, type=str)
