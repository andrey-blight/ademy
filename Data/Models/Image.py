from Classes.SqlAlchemyDatabase import SqlAlchemyDatabase, SqlAlchemyBase

from sqlalchemy import Column, Integer, CheckConstraint, ForeignKey, String
from sqlalchemy.orm import relationship
from sqlalchemy_serializer import SerializerMixin


class Image(SqlAlchemyBase, SerializerMixin):
    __tablename__ = "images"
    __table_args__ = (
        CheckConstraint("count <= 5", name="check_count_for_one_user"),
    )
    serialize_only = ("id", "user_id", "count", "image_href")

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    image_href = Column(String(100), nullable=False)
    count = Column(Integer)
    user = relationship("User")

    def __init__(self, user_id, image_href):
        self.user_id = user_id
        self.image_href = image_href
        self.set_index()

    def set_index(self, session=None) -> None:
        """Add account number of image"""
        if session is None:
            database = SqlAlchemyDatabase()
            session = database.create_session()
        self.count = session.query(Image).where(self.user_id == Image.user_id).count() + 1
