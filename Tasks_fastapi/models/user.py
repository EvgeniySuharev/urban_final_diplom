from backend.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Integer, String, Column
from models import task


class User(Base):
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    password = Column(String)

    tasks = relationship('Task', back_populates='user')


"""Модель таблицы БД. Наследуется от базового класса. В ней указаны название таблицы,
название и содержание колонок, а так же описана связь с таблицей Task.
"""