from django.contrib.auth.models import AbstractUser
from django.db import models


class CIUser(AbstractUser):
    is_doctor = models.BooleanField('Врач', blank=True, null=True)
