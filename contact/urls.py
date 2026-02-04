from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DiscussProjectViewSet

router = DefaultRouter()
router.register(r'discuss-project', DiscussProjectViewSet, basename='discuss-project')

urlpatterns = [
    path('', include(router.urls)),
]
