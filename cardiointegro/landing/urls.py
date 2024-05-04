from django.urls import path

from . import views

app_name = 'landing'

urlpatterns = [
    path('', views.MainPageTemplateView.as_view(), name='main_page'),
    path('tutorial/', views.TutorialTemplateView.as_view(), name='tutorial'),
]
