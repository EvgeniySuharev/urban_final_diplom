from django.shortcuts import render, HttpResponseRedirect
from .models import Task


# Create your views here.
def index(request):
    context = {
        'title': 'Главная страница'
    }
    return render(request, 'tasks/base.html', context)


"""Функция отображает в браузере html страницу
"""


def tasks(request):
    all_tasks = Task.objects.all()
    all_tasks = all_tasks.filter(user=request.user)
    context = {'all_tasks': all_tasks,
               'title': 'Мои задачи'}
    return render(request, 'tasks/tasks.html', context)


"""Функция выполняет подключение к БД и выводит в html шаблон список
задач для текущего пользователя
"""


def add_task(request):
    user = request.user
    title = request.POST['title']
    description = request.POST['description']
    Task.objects.create(user=user, title=title, description=description)
    return HttpResponseRedirect('/tasks/')


"""Функция принимает данные из полей формы на странице и создает задачу, связывая
ее с текущим пользователем
"""


def delete_task(request, task_id):
    task = Task.objects.get(id=task_id)
    task.delete()
    return HttpResponseRedirect('/tasks/')


"""Функция принимает id задачи, выполняет подключение к БД и удаляет объект в таблице Task
с указанным id.
"""
