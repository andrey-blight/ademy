from Classes.SqlAlchemyDatabase import SqlAlchemyDatabase, SqlAlchemyBase

from sqlalchemy import Column, Integer, CheckConstraint, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects import mysql
from sqlalchemy_serializer import SerializerMixin


class Image(SqlAlchemyBase, SerializerMixin):
    __tablename__ = "images"
    __table_args__ = (
        CheckConstraint("count <= 5", name="check_count_for_one_user"),
    )
    serialize_only = ("id", "user_id", "count", "image")

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    image = Column(mysql.MEDIUMBLOB, nullable=False)
    count = Column(Integer)
    user = relationship("User")

    def __init__(self, user_id, image):
        self.user_id = user_id
        self.image = image
        self.set_index()

    def set_index(self):
        """Add account number of image"""
        database = SqlAlchemyDatabase()
        session = database.create_session()
        self.count = session.query(Image).where(self.user_id == Image.user_id).count() + 1
