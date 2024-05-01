from django.urls import path

from . import views

app_name = 'users'

urlpatterns = [
    path('registration/', views.CreateUserView.as_view(), name='registration'),
    path('logout/', views.logout_view, name='logout'),
]
