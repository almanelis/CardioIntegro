from django.urls import path

from . import views

app_name = 'main'

urlpatterns = [
    # Приложение главной страницы
    path('', views.MainPageView.as_view(), name='index'),
]
