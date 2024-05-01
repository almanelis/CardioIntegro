from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Модель пользователя"""
    is_doctor = models.BooleanField('Медицинский работник', blank=True, null=True)
