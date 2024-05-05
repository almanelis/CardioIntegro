from django.urls import path

from . import views

app_name = 'landing'

urlpatterns = [
    path('', views.MainPageTemplateView.as_view(), name='main_page'),
    path('knowledgebase/', views.TutorialTemplateView.as_view(),
         name='knowledgebase'),
    path('frontend/', views.FrontendTemplateView.as_view()),
]
