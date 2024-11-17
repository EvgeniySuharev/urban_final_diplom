from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import User


class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ('username', 'password')


class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name',
                  'username', 'password1', 'password2')


"""Классы для формирования в шаблоне формы авторизации и регистрации.
Наследуются от встроенных в django классов AuthenticationForm и UserCreationForm.
В них указано какие поля будут отображены для ввода на html странице
"""