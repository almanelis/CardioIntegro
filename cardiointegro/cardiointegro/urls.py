from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Основное приложение
    path('', include('main.urls'), name='main'),
    # Приложение пользователя
    path('users/', include('users.urls')),
    # Приложение для управления профилем
    path('auth/', include('django.contrib.auth.urls'), name='users'),
    # Приложение админки
    path('admin/', admin.site.urls),
    # Автоматическое обновление страниц для фронтенда
    path("__reload__/", include("django_browser_reload.urls")),
]
