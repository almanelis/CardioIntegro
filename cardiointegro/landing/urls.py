from django.urls import path

from . import views

app_name = 'landing'

urlpatterns = [
    path('', views.feedback_view, name='main_page'),
    path('knowledgebase/', views.TutorialTemplateView.as_view(),
         name='knowledgebase'),
]
