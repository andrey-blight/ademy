from Classes.SqlAlchemyDatabase import SqlAlchemyBase

from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint, Table
from sqlalchemy.orm import relationship

user_to_interest = Table("user_to_interest", SqlAlchemyBase.metadata,
                         Column("user_id", Integer, ForeignKey("users.id")),
                         Column("interest_id", Integer, ForeignKey("interests.id"), ),
                         UniqueConstraint("user_id", "interest_id", name="unique_value"))


class Interest(SqlAlchemyBase):
    __tablename__ = "interests"
    id = Column(Integer, primary_key=True)
    name = Column(String(25), unique=True)

    users = relationship("User", secondary=user_to_interest, back_populates="interests")

    def __init__(self, name):
        self.name = name
