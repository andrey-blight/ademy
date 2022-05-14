from Classes.SqlAlchemyDatabase import SqlAlchemyBase
from Data.Models.Message import Message

from sqlalchemy import Column, Integer, ForeignKey, Table, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy_serializer import SerializerMixin

chat_to_user = Table("chat_to_user", SqlAlchemyBase.metadata,
                     Column("user_id", Integer, ForeignKey("users.id")),
                     Column("chat_id", Integer, ForeignKey("chats.id")),
                     UniqueConstraint("user_id", "chat_id", name="unique_value"))


class Chat(SqlAlchemyBase, SerializerMixin):
    __tablename__ = "chats"
    serialize_only = ("id", "last_message", "last_message_created_at", "users")

    id = Column(Integer, primary_key=True)
    last_message_id = Column(Integer, ForeignKey("messages.id"), nullable=True)
    users = relationship("User", secondary=chat_to_user, back_populates="chats")
    last_message = relationship("Message", foreign_keys=[last_message_id])
    messages = relationship("Message", cascade="all, delete", back_populates="chat", foreign_keys=[Message.chat_id])
