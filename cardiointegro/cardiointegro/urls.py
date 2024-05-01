from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('main.urls')),
    path('auth/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
    path('user/', include('user.urls')),
    path("__reload__/", include("django_browser_reload.urls")),
]
