from django.contrib import admin

from .models import FeedbackModel


@admin.register(FeedbackModel)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'email',
        'created_at',
    )
