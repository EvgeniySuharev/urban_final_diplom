from starlette.middleware.sessions import SessionMiddleware
from fastapi import FastAPI, Request, Depends, status, Form
from fastapi.templating import Jinja2Templates
from backend.db_depends import get_db
from typing import Annotated
from sqlalchemy.orm import Session
from sqlalchemy import insert, select, delete
from models.user import User
from models.task import Task
from fastapi.responses import RedirectResponse


SECRET_KEY = 'ckqho2oi2992bcoqwcbb892t6cscpoqc0f0997vcgj'
app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)
templates = Jinja2Templates(directory='templates')
"""Создаем приложение app, указываем ключ для работы с сессиями.
Назначаем переменную templates для работы с шаблонизатором Jinja2"""


@app.get('/')
async def home(request: Request):
    context = {
        'request': request,
        'title': 'Главная'
    }
    return templates.TemplateResponse('tasks/base.html', context)
"""Функция принимает запрос и возвращает в браузер html шаблон.
"""


@app.get('/create_user/')
async def create_user(request: Request):
    context = {
        'request': request,
        'title': 'Зарегистрироваться',
    }
    return templates.TemplateResponse('users/registration.html', context)
"""Функция принимает запрос и возвращает в браузер html шаблон.
"""


@app.post('/register')
async def register_user(request: Request,
                        db: Annotated[Session, Depends(get_db)],
                        name=Form(),
                        password1=Form(),
                        password2=Form()):
    context = {
        'request': request,
        'title': 'Зарегистрироваться',
    }
    res = db.execute(select(User))
    users = res.scalars().all()
    for user in users:
        if user.name == name:
            context['msg'] = f'Пользователь {name} уже существует'
            return templates.TemplateResponse('users/registration.html', context)
    if password1 == password2:
        query = insert(User).values(
            name=name,
            password=password1,
        )
        db.execute(query)
        db.commit()
        context['msg'] = f'Пользователь {name} зарегистрирован'
    else:
        context['msg'] = 'Пароли не совпадают'
    return templates.TemplateResponse('users/registration.html', context)
"""Функция принимает данные из формы в html документе, выполняет подключение к БД, и
создает объект в таблице User
"""


@app.get('/login_form')
async def login_form(request: Request):
    context = {
        'request': request,
        'title': 'Авторизация',
    }
    return templates.TemplateResponse('users/login.html', context)
"""Функция принимает запрос и возвращает в браузер html шаблон.
"""


@app.post('/login')
async def login(request: Request,
                db: Annotated[Session, Depends(get_db)],
                name=Form(), psw=Form()):
    context = {
        'request': request,
        'title': 'Авторизация',
    }
    res = db.execute(select(User))
    users = res.scalars().all()
    for user in users:
        if user.name == name:
            if user.password == psw:
                request.session['user'] = user.id
                return RedirectResponse('/all_tasks/', status_code=status.HTTP_302_FOUND)
    context['msg'] = 'Имя пользователя или пароль введены неправильно'
    return templates.TemplateResponse('users/login.html', context)
"""Функция принимает данные из полей формы на странице авторизации, выполняет подключение
к БД. Если пользователь с таким именем и паролем найден в БД, то выполняется авторизация
пользователя на сервере.
"""


@app.get('/logout')
async def logout(request: Request):
    try:
        del request.session['user']
    except KeyError:
        return {'message': 'not authenticated'}
    return RedirectResponse('/login_form')
"""Функция выполняет выход пользователя из профиля, если он авторизован
"""


@app.post('/create_task')
async def create_task(request: Request,
                      db: Annotated[Session, Depends(get_db)],
                      title=Form(max_length=20),
                      content=Form()):
    if 'user' in request.session:
        query = insert(Task).values(
            title=title,
            content=content,
            user_id=request.session['user']
        )
        db.execute(query)
        db.commit()
        return RedirectResponse('/all_tasks/', status_code=status.HTTP_302_FOUND)
    else:
        return {'message': 'not authenticated'}
"""Функция принимает данные из полей на html странице, выполняет подключение к БД и
создает новую задачу. При этом в колонке user_id указывается id текущего авторизованного
пользователя
"""


@app.get('/all_tasks/')
async def all_tasks(request: Request,
                    db: Annotated[Session, Depends(get_db)]):
    if 'user' in request.session:
        res = db.execute(select(Task).filter_by(user_id=request.session['user']))
        tasks = res.scalars().all()
        context = {
            'request': request,
            'title': 'Мои задачи',
            'all_tasks': tasks
        }
        print(request.session['user'])
        return templates.TemplateResponse('tasks/tasks.html', context)
    else:
        return RedirectResponse('/login_form')
"""Функция выполняет подключение к БД и выводит на html шаблон все задачи
текущего авторизованного пользователя
"""


@app.post('/delete_task/{task_id}')
async def delete_task(request: Request,
                      db: Annotated[Session, Depends(get_db)],
                      task_id: int):
    if 'user' in request.session:
        query = delete(Task).where(Task.id == task_id)
        db.execute(query)
        db.commit()
        return RedirectResponse('/all_tasks/', status_code=status.HTTP_302_FOUND)
    else:
        return {'message': 'not authenticated'}
"""Функция принимает id задачи, выполняет подключение к БД и удаляет
строку с указанным id из таблицы tasks
"""
