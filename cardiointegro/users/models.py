from django.contrib.auth.models import AbstractUser
from django.db import models


class CIUser(AbstractUser):
    """Абстрактная модель пользователя"""
    is_doctor = models.BooleanField('Вы медицинский работник?',
                                    blank=True, null=True)
    email = models.EmailField('Адрес электронной почты', blank=True, null=True)
