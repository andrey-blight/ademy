from Classes.SqlAlchemyDatabase import SqlAlchemyBase, SqlAlchemyDatabase

from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, CheckConstraint, Table, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy_serializer import SerializerMixin
from werkzeug.security import generate_password_hash, check_password_hash

liked_to = Table("liked_to", SqlAlchemyBase.metadata,
                 Column("id", Integer, ForeignKey("users.id")),
                 Column("id_to", Integer, ForeignKey("users.id")),
                 UniqueConstraint("id", "id_to", name="unique_value_to"))
liked_from = Table("liked_from", SqlAlchemyBase.metadata,
                   Column("id", Integer, ForeignKey("users.id")),
                   Column("id_from", Integer, ForeignKey("users.id")),
                   UniqueConstraint("id", "id_from", name="unique_value_from"))


class User(SqlAlchemyBase, SerializerMixin):
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
    liked_to = relationship("User",
                            secondary="liked_to",
                            primaryjoin=(id == liked_to.c.id),
                            secondaryjoin=(id == liked_to.c.id_to)
                            )  # Все пользователи которым текущий пользователь поставил лайк
    liked_from = relationship("User",
                              secondary="liked_from",
                              primaryjoin=(id == liked_from.c.id),
                              secondaryjoin=(id == liked_from.c.id_from)
                              )  # Все пользователи которые поставили лайк текущему пользователю

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

    def set_like(self, id: int, session=None) -> None:
        """Set like to user_to from current user and set user_to like from current user"""
        if session is None:
            database = SqlAlchemyDatabase()
            session = database.create_session()
        user_to = session.query(User).get(id)
        self.liked_to.append(user_to)
        user_to.liked_from.append(self)
        session.commit()

    def __repr__(self) -> str:
        return str(self.to_dict())
