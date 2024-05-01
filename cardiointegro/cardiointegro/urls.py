from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('main.urls'), name='main'),
    path('users/', include('users.urls')),
    path('auth/', include('django.contrib.auth.urls'), name='users'),
    path('admin/', admin.site.urls),
    path("__reload__/", include("django_browser_reload.urls")),
]
