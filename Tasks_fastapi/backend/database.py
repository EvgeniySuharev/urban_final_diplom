from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase


class Base(DeclarativeBase):
    pass


engine = create_engine('sqlite:///taskmanager.db', echo=True)
SessionLocal = sessionmaker(bind=engine)

"""Создаем базовый класс, от которого будут наследоваться будущие модели(таблицы).
Создаем локальную сессию для осуществления подключения к БД"""