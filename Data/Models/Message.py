from Classes.SqlAlchemyDatabase import SqlAlchemyBase

from datetime import datetime

from sqlalchemy import Column, Integer, ForeignKey, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy_serializer import SerializerMixin


class Message(SqlAlchemyBase, SerializerMixin):
    __tablename__ = "messages"
    serialize_only = ("id", "text", "created_at")

    id = Column(Integer, primary_key=True)
    chat_id = Column(Integer, ForeignKey("chats.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    text = Column(String(500), nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    chat = relationship("Chat")
    user = relationship("User")

    def __init__(self, text, chat_id, user_id):
        self.text = text
        self.chat_id = chat_id
        self.user_id = user_id
