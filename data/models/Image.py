from Classes.SqlAlchemyDatabase import SqlAlchemyDatabase

from sqlalchemy import Column, Integer, CheckConstraint, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects import mysql

database = SqlAlchemyDatabase()


class Image(database.get_base()):
    __tablename__ = "images"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    image = Column(mysql.MEDIUMBLOB, nullable=False)
    count = Column(Integer)
    user = relationship("User")

    __table_args__ = (
        CheckConstraint("count <= 5', name='check_count_for_one_user"),
    )

    def __init__(self, user_id, image):
        self.user_id = user_id
        self.image = image
        self.set_index()

    def set_index(self):
        session = database.create_session()
        self.count = session.query(Image).where(self.user_id == Image.user_id).count() + 1
