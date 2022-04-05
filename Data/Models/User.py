from Classes.SqlAlchemyDatabase import SqlAlchemyBase

from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, CheckConstraint
from sqlalchemy.orm import relationship
from sqlalchemy_serializer import SerializerMixin
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(SqlAlchemyBase, SerializerMixin, UserMixin):
    __tablename__ = "users"
    __table_args__ = (
        CheckConstraint("sex IN (1, 2)", name="check_sex"),  # if sex is 1 - Male else sex is Female (ISO/IEC 5218)
    )
    serialize_only = ("id", "name", "surname", "age", "about_yourself",
                      "sex", "hashed_password", "email", "created_at", "updated_at", "images", "interests")

    id = Column(Integer, primary_key=True)
    name = Column(String(25), nullable=False)
    surname = Column(String(25), nullable=False)
    age = Column(String(25), nullable=False)
    about_yourself = Column(String(2000))
    sex = Column(Integer, nullable=False)
    hashed_password = Column(String(200), nullable=False)
    email = Column(String(25), unique=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    images = relationship("Image", cascade="all, delete", back_populates="user")
    interests = relationship("Interest", secondary="user_to_interest", back_populates="users")

    def __init__(self, name: str, surname: str, age: int, sex: int in [1, 2], password: str, email: str,
                 about_yourself=None):
        self.name = name
        self.surname = surname
        self.age = age
        self.about_yourself = about_yourself
        self.sex = sex
        self.email = email
        self._set_password(password)

    def _set_password(self, password: str) -> None:
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.hashed_password, password)

    def __repr__(self) -> str:
        return str(self.to_dict())
