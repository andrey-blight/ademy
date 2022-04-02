from Classes.SqlAlchemyDatabase import SqlAlchemyBase

from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, CheckConstraint, Table
from sqlalchemy.orm import relationship
from sqlalchemy_serializer import SerializerMixin
from werkzeug.security import generate_password_hash, check_password_hash


class Like(SqlAlchemyBase):
    __tablename__ = "likes"
    id = Column(Integer, primary_key=True)
    user_from = Column(Integer, ForeignKey("users.id"))
    user_to = Column(Integer, ForeignKey("users.id"))
    user_from_rel = relationship("User", foreign_keys=[user_from])
    user_to_rel = relationship("User", foreign_keys=[user_to])


#
# like = Table("user_likes", SqlAlchemyBase.metadata,
#              Column("id", Integer, primary_key=True),
#              Column("user_from", Integer, ForeignKey("users.id")),
#              Column("user_to", Integer, ForeignKey("users.id")))


class User(SqlAlchemyBase, SerializerMixin):
    __tablename__ = "users"
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
    images = relationship("Image", back_populates="user")
    interests = relationship("Interest", secondary="user_to_interest", back_populates="users")
    # TODO: создать связь между тем кого лайкнул пользователь и тех кто лайкнул пользователя
    liked_from = relationship("Like",
                              primaryjoin="User.id == Like.user_to",
                              )
    liked_to = relationship("Like",
                            primaryjoin="User.id == Like.user_from",
                            )
    __table_args__ = (
        CheckConstraint("sex IN (1, 2)", name="check_sex"),  # if sex is 1 - Male else sex is Female (ISO/IEC 5218)
    )

    def __init__(self, name: str, surname: str, age: int, sex: int in [1, 2], password: str, email: str):
        self.name = name
        self.surname = surname
        self.age = age
        self.sex = sex
        self.email = email
        self._set_password(password)

    def _set_password(self, password: str) -> None:
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.hashed_password, password)

    def __repr__(self) -> str:
        return str(self.to_dict())
