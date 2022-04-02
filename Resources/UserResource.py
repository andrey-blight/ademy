from Classes.Model import Model

from flask import jsonify


class UserResource(Model):
    def __init__(self):
        super().__init__("User")

    # Returns the user by id
    def get(self, user_id: int):
        self.is_id_exists(user_id)
        user = self.session.query(self.Model).get(user_id)
        if user:
            return jsonify({user.to_dict()})
        else:
            return jsonify({"message": "Error"})

    def put(self, user_id: int):
        self.is_id_exists(user_id)
        self.parser.add_argument("name", required=False, type=str)
        self.parser.add_argument("surname", required=False, type=str)
        self.parser.add_argument("age", required=False, type=int)
        self.parser.add_argument("sex", required=False, type=int)
        self.parser.add_argument("password", required=False, type=str)
        self.parser.add_argument("email", required=False, type=str)
        args = self.parser.parse_args()
        user = self.session.query(self.Model).get(user_id)
        for arg in args:
            if args[arg] is not None:
                setattr(user, arg, args[arg])
        self.session.commit()
        return jsonify(user.to_dict())

    def delete(self, user_id: int):
        session = self.db.create_session()
        user = session.query(self.Model).delete(user_id)
        session.commit()
        return jsonify(user.to_dict())
