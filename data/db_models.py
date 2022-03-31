from .db_session import SqlAlchemyBase, create_session

from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, CheckConstraint, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.dialects import mysql
from werkzeug.security import generate_password_hash, check_password_hash


class User(SqlAlchemyBase):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(25), nullable=False)
    surname = Column(String(25), nullable=False)
    age = Column(String(25), nullable=False)
    sex = Column(Integer, nullable=False)
    hashed_password = Column(String(200), nullable=False)
    created_on = Column(DateTime, default=datetime.now)
    updated_on = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    images = relationship("Image", back_populates="user")

    __table_args__ = (
        CheckConstraint('sex IN (1, 2)', name='check_sex'),  # if sex is 1 - Male else sex is Female (ISO/IEC 5218)
    )

    def __init__(self, name, surname, age, sex, password):
        self.name = name
        self.surname = surname
        self.age = age
        self.sex = sex
        self._set_password(password)

    def _set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)


class Image(SqlAlchemyBase):
    __tablename__ = 'images'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    image = Column(mysql.MEDIUMBLOB, nullable=False)
    index = Column(Integer)
    user = relationship("User")

    __table_args__ = (
        CheckConstraint('index <= 5', name='check_count_for_one_user'),
        UniqueConstraint('user_id', 'image', name='unique_ssn')
    )

    def __init__(self, user_id, image):
        self.user_id = user_id
        self.image = image
        self.set_index()

    def set_index(self):
        session = create_session()
        self.index = session.query(Image).where(self.user_id == Image.user_id).count() + 1
