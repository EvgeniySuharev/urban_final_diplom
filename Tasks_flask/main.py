from flask import Flask, render_template, request, redirect, url_for, flash, session
from db import db
from models import User, Task
from werkzeug.security import generate_password_hash, check_password_hash

"""Создаем наше приложение. В настройках указываем путь к БД.
Инициализируем класс расширения SQLAlchrmy в приложении app,
вызвав метод db.init_app. И далее создаем таблицы, определенные моделями
в файле models.py
"""
app = Flask(__name__)
app.config['SECRET_KEY'] = 'con29uanjohfg93hv92'
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///flask_taskmanager.db'
db.init_app(app)
with app.app_context():
    db.create_all()


@app.route('/')
def index():
    context = {
        'title': 'Главная страница'
    }
    """Функция выводит в браузер страницу base.html
    с контекстом, указанным в словаре context
    """
    return render_template('base.html', context=context)


@app.route('/register', methods=['POST', 'GET'])
def register():
    if 'current_user' in session:
        flash('Вы уже авторизованы. Выйдите из профиля, чтобы зарегистрировать нового'
              'пользователя', 'error')
        return redirect(url_for('index'))
    if request.method == 'POST':
        users = db.session.execute(db.select(User)).scalars().all()
        for user in users:
            if user.name == request.form['name']:
                flash('Пользователь с таким именем уже зарегистрирован', 'error')
                return redirect('register')
        if request.form['password1'] != request.form['password2']:
            flash('Пароли не совпадают', 'error')
        else:
            psw = generate_password_hash(request.form['password1'])
            user = User(
                name=request.form['name'],
                password=psw
            )
            db.session.add(user)
            db.session.commit()
            flash(f'Пользователь {request.form['name']} зарегистрирован', 'success')
    context = {
        'title': 'Форма регистрации'
    }
    """Если метод запроса - post, то производится проверка данных из формы, подключение к БД
    и добавление нового пользователя в таблицу users. Если метод - get, то выводится страница
    с формой"""
    return render_template('registration.html', context=context)


@app.route('/login', methods=['POST', 'GET'])
def login():
    if 'current_user' in session:
        flash('Вы уже авторизованы', 'error')
        return redirect(url_for('index'))
    if request.method == 'POST':
        name = request.form['name']
        query = db.select(User).filter_by(name=name)
        try:
            user = db.session.execute(query).scalar_one()
        except Exception:
            flash('Имя пользователя указано неверно', 'error')
            return redirect(url_for('login'))
        if check_password_hash(user.password, request.form['password']):
            session['current_user'] = user.id
            flash('Авторизация прошла успешно', 'success')
            return redirect(url_for('index'))
        flash('Пароль указан неверно', 'error')
    context = {
        'title': 'Форма авторизации'
    }
    """Если метод запроса - GET выводит страницу с формой. Если метод - POST, принимает данные
    из формы и сверяет с БД. Если пользователь с таким именем и паролем найден, то происходит
    авторизация
    """
    return render_template('login.html', context=context)


@app.route('/logoff')
def logoff():
    try:
        del session['current_user']
    except KeyError:
        flash('Вы не авторизованы', 'error')
    """Если пользователь авторизован, производит выход из текущего профиля"""
    return redirect(url_for('login'))


@app.route('/all_tasks', methods=['POST', 'GET'])
def get_all_tasks():
    if 'current_user' not in session:
        flash('Страница доступна только для авторизованного пользователя', 'error')
        return redirect(url_for('login'))
    if request.method == 'POST':
        task = Task(
            title=request.form['title'],
            content=request.form['content'],
            user_id=int(session['current_user'])
        )
        db.session.add(task)
        db.session.commit()
    res = db.session.execute(db.select(Task).filter_by(user_id=session['current_user']))
    tasks = res.scalars().all()
    context = {
        'title': 'Главная страница',
        'tasks': tasks
    }
    """Если метод запроса - GET, функция выполняет подключение к БД и 
    передает в контекст список объектов из таблицы task, затем выводит
    в браузер страницу html с определенным контекстом для шаблона.
    Если же метод - POST, то в таблицу task из БД добавляется объект,
    аттрибуты для которого берутся из заполненной на странице формы.
    """
    return render_template('tasks.html', context=context)


@app.route('/delete_task/<int:task_id>', methods=['POST'])
def delete_task_by_id(task_id):
    task = db.get_or_404(Task, task_id)
    db.session.delete(task)
    db.session.commit()
    """Функция принимает из запроса id объекта таблицы task,
    находит, данный объект в БД по id и удалет. Затем функция redirect
    перенаправляет на функцию get_all_tasks, которая выводит актуальный список
    объектов из таблицы task.
    """
    return redirect(url_for('get_all_tasks'))


if __name__ == '__main__':
    app.run(debug=True)
