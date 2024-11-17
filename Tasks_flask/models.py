from db import Base
from sqlalchemy import Column, Integer, ForeignKey, String


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    password = Column(String)


class Task(Base):
    __tablename__ = "task"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    content = Column(String)
    user_id = Column(Integer, ForeignKey(User.id))
