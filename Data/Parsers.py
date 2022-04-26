from flask_restful import reqparse

user_parser = reqparse.RequestParser()
user_parser.add_argument("name", required=True, type=str)
user_parser.add_argument("surname", required=True, type=str)
user_parser.add_argument("age", required=True, type=int)
user_parser.add_argument("about_yourself", required=False, type=str)
user_parser.add_argument("sex", required=True, type=int)
user_parser.add_argument("password", required=True, type=str)
user_parser.add_argument("email", required=True, type=str)
user_parser.add_argument("interests", required=True, type=str, action="append")

user_edit_parser = reqparse.RequestParser()
user_edit_parser.add_argument("name", required=False, type=str)
user_edit_parser.add_argument("surname", required=False, type=str)
user_edit_parser.add_argument("age", required=False, type=int)
user_edit_parser.add_argument("about_yourself", required=False, type=str)
user_edit_parser.add_argument("sex", required=False, type=int)
user_edit_parser.add_argument("password", required=False, type=str)
user_edit_parser.add_argument("email", required=False, type=str)

image_parser = reqparse.RequestParser()
image_parser.add_argument("image_href", required=True, type=str)

image_edit_parser = reqparse.RequestParser()
image_edit_parser.add_argument("user_id", required=False, type=int)
image_edit_parser.add_argument("image_href", required=False, type=str)

interest_parser = reqparse.RequestParser()
interest_parser.add_argument("name", required=True, type=str)

message_parser = reqparse.RequestParser()
message_parser.add_argument("text", required=True, type=str)
message_parser.add_argument("user_id", required=True, type=int)
