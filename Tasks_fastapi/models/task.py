from backend.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Integer, ForeignKey, String, Column
from models import user


class Task(Base):
    __tablename__ = 'tasks'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    content = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'),
                     nullable=False,
                     index=True)

    user = relationship('User', back_populates='tasks')


"""Модель таблицы БД. Наследуется от базового класса. В ней указаны название таблицы,
название и содержание колонок, а так же описана связь с таблицей User.
"""
