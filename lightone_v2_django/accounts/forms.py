from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


class SignupForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ('username', 'name', 'password1', 'password2')
        labels = {
            'username': '아이디',
            'name': '이름',
            'password1': '비밀번호',
            'password2': '비밀번호 확인',
        }
        help_texts = {
            'username': None,
            'name': None,
            'password1': None,
            'password2': None,
        }
