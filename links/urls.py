"""
URL configuration for links app.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NegativeLinkViewSet

router = DefaultRouter()
router.register(r'links', NegativeLinkViewSet, basename='negativelink')

urlpatterns = [
    path('', include(router.urls)),
]
