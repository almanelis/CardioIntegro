from django.urls import path

from . import views

app_name = 'users'

urlpatterns = [
    # Регистрация
    path('registration/', views.CreateUserView.as_view(), name='registration'),
    # Аутентификация
    path('logout/', views.logout_view, name='logout'),
]
