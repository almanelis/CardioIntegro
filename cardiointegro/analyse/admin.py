from django.contrib import admin

from .models import ECGAnalyse


@admin.register(ECGAnalyse)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'doctor',
        'created_at',
    )
