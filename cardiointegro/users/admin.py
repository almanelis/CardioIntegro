from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CIUser

UserAdmin.fieldsets += (
    ('Extra Fields', {'fields': ('is_doctor',)}),
)

admin.site.register(CIUser)
