from django.urls import path

from . import views

app_name = 'analyse'

urlpatterns = [
    # Вывод списка анализов ЭКГ
    path('list/', views.analyse_list_view, name='list'),
    # Форма создания анализа ЭКГ
    path('create/', views.analyse_create_view, name='create'),
    # Вывод отчёта по анализу ЭКГ
    path('<int:pk>/', views.AnalyseDetailView.as_view(), name='detail'),
    # Поиск среди спика анализов ЭКГ
    path('search/', views.analyse_search_view, name='search'),
]
