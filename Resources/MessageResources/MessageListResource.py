from Classes.Model import Model
from Data.Models.User import User
from Data.Models.Message import Message
from Data.Parsers import message_parser

from flask import jsonify
from flask.wrappers import Response
from flask_restful import abort


class MessageListResource(Model):
    def __init__(self):
        super().__init__("Chat")  # init as a chat

    def get(self, chat_id: int):
        """
        Get all messages in chat ordered by create time (first are newest)
        :param chat_id: id of needed chat
        :return: JSON list with messages ordered by create time
        """
        session = self.db.create_session()
        chat = self.get_object(chat_id, session)
        if chat is None:
            abort(404, message=f"Chat {chat_id} not found")
        messages = sorted(chat.messages, reverse=True, key=lambda el: el.created_at)
        return jsonify([item.to_dict() for item in messages])

    def post(self, chat_id: int) -> Response:
        """
        Add message to chat. Need to pass in body structure {text: "Message text", user_id: id}
        All spaces at the beginning and end of the text are removed
        :param chat_id: id of needed chat
        :return: JSON response with status of request
        """
        session = self.db.create_session()
        args = message_parser.parse_args()
        chat = self.get_object(chat_id, session)
        user = session.query(User).get(args["user_id"])
        if chat is None:
            abort(404, message=f"Chat {chat_id} not found")
        if user is None:
            abort(404, message=f"User {args['user_id']} not found")
        try:
            if user not in chat.users:
                return jsonify({"error": f"user {args['user_id']} does not have access to the chat {chat_id}"})
            args["text"] = args["text"].strip()  # delete spaces
            if not args["text"]:
                return jsonify({"error": f"text is not filled in"})
            message = Message(text=args["text"], chat_id=chat_id, user_id=args["user_id"])
            session.add(message)
            session.commit()
            message.chat.last_message_id = message.id
            session.commit()
            return jsonify({"message": f"Message {args['text']} was added to chat {chat_id}"
                                       f" from user {args['user_id']}"})
        except Exception as ex:
            session.rollback()
            print(ex)
            return jsonify({"error": "Unexpected"})
