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
    text = Column(String(200), nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    chat = relationship("Chat")
