from Classes.Model import Model
from Data.Models.Chat import Chat
from Data.Models.Message import Message
from Data.Functions import token_required
from Data.Parsers import message_parser

from flask import jsonify
from flask.wrappers import Response


class MessageListResource(Model):
    def __init__(self):
        super().__init__("Message")

    @token_required
    def get(self, chat_id: int):
        session = self.db.create_session()
        chat = session.query(Chat).get(chat_id)
        messages = chat.messages
        return jsonify([item.to_dict() for item in messages])

    @token_required
    def post(self, chat_id: int) -> Response:
        session = self.db.create_session()
        try:
            args = message_parser.parse_args()
            message = Message(text=args["text"], chat_id=chat_id,
                              user_id=args["user_id"])
            session.add(message)
            session.commit()
            message.chat.last_message = args["text"]
            session.commit()
            return jsonify({"message": f"Message {args['text']} "
                                       f"was added to chat {chat_id}"
                                       f" from user {args['user_id']}"})
        except Exception as ex:
            session.rollback()
            print(ex)
            return jsonify({"Error": "Unexpected"})
