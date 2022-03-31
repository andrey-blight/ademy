from ..db_session import SqlAlchemyBase

from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, CheckConstraint
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash


class User(SqlAlchemyBase):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(25), nullable=False)
    surname = Column(String(25), nullable=False)
    age = Column(String(25), nullable=False)
    sex = Column(Integer, nullable=False)
    hashed_password = Column(String(200), nullable=False)
    email = Column(String(25), unique=True)
    created_on = Column(DateTime, default=datetime.now)
    updated_on = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    images = relationship("Image", back_populates="user")
    interests = relationship('Interest', secondary='user_to_interest', back_populates='users')

    __table_args__ = (
        CheckConstraint('sex IN (1, 2)', name='check_sex'),  # if sex is 1 - Male else sex is Female (ISO/IEC 5218)
    )

    def __init__(self, name, surname, age, sex, password, email):
        self.name = name
        self.surname = surname
        self.age = age
        self.sex = sex
        self.email = email
        self._set_password(password)

    def _set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)
