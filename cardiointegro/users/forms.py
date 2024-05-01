from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class RegisterForm(UserCreationForm):
    # Вывод в форму дополнительных полей
    email = forms.EmailField(required=True, label='Адрес электронной почты')

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'is_doctor',)
