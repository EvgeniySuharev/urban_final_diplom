from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    pass


"""Класс (модель) для таблицы с пользователями в БД. Наследуется от
встроенного в django класса AbstractUser в котором уже указаны все
необходимые поля для таблицы
"""