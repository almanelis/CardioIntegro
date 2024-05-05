from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

from . import settings

urlpatterns = [
    # Лендинги
    path('', include('landing.urls'), name='landing'),
    # Приложение для анализа ЭКГ
    path('analyse/', include('analyse.urls'), name='analyse'),
    # Приложение пользователя
    path('users/', include('users.urls')),
    # Приложение для управления профилем
    path('auth/', include('django.contrib.auth.urls'), name='users'),
    # Приложение админки
    path('admin/', admin.site.urls),
    # Автоматическое обновление страниц для фронтенда
    # Автоматическое обновление страниц для фронтенда
    path("__reload__/", include("django_browser_reload.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
