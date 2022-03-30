from .db_session import SqlAlchemyBase

from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, CheckConstraint


class User(SqlAlchemyBase):
    __tablename__ = 'users'
    id = Column(Integer(), primary_key=True)
    name = Column(String(25), nullable=False)
    surname = Column(String(25), nullable=False)
    age = Column(String(25), nullable=False)
    sex = Column(Integer())
    created_on = Column(DateTime(), default=datetime.now)
    updated_on = Column(DateTime(), default=datetime.now, onupdate=datetime.now)
    __table_args__ = (
        CheckConstraint('sex IN (1, 2)'),  # if sex is 1 - Male else sex is Female (ISO/IEC 5218)
    )
