"""
URL configuration for stats app.
"""
from django.urls import path
from .views import DashboardStatsView, PlatformStatsView

urlpatterns = [
    path('stats/dashboard/', DashboardStatsView.as_view(), name='dashboard-stats'),
    path('stats/platform/<str:platform>/', PlatformStatsView.as_view(), name='platform-stats'),
]
