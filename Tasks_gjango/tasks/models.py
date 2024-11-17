from django.db import models
from users.models import User


# Create your models here.
class Task(models.Model):
    title = models.CharField(max_length=40)
    description = models.TextField()
    time_stamp = models.DateTimeField(auto_now_add=True)
    is_finished = models.BooleanField(default=False)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)


"""Класс (модель) таблицы Task в БД. В нем указаны названия и типы данных колонок
таблицы. Так же описана связь с таблицей User"""