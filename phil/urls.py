"""
URL configuration for phil project.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('links.urls')),
    path('api/', include('stats.urls')),
]
