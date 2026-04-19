
from django.contrib import admin
from django.urls import path, include



urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/films/', include('films.urls')),
    path('api/v1/users/', include('users.urls')),
]
