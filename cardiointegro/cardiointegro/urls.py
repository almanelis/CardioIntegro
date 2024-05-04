from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

from . import settings

urlpatterns = [
    path('', include('landing.urls'), name='landing'),
    # Основное приложение
    path('analyse/', include('analyse.urls'), name='analyse'),
    # Приложение пользователя
    path('users/', include('users.urls')),
    # Приложение для управления профилем
    path('auth/', include('django.contrib.auth.urls'), name='users'),
    # Приложение админки
    path('admin/', admin.site.urls),
    # Автоматическое обновление страниц для фронтенда
    path("__reload__/", include("django_browser_reload.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
