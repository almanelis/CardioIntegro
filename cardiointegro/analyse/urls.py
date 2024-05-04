from django.urls import path

from . import views

app_name = 'analyse'

urlpatterns = [
    path('list/', views.analyse_list_view, name='list'),
    path('create/', views.analyse_create_view, name='create'),
    path('<int:pk>/', views.AnalyseDetailView.as_view(), name='detail')
]
