from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)
"""Назначаем базовый класс Base, от которого будут наследоваться
модели таблиц БД. Назначаем переменную db, которая является
экземпляром класса SQLAlchemy из расширения flask_sqlalchemy
"""