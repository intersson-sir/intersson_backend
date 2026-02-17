"""
Views for the stats app.
"""
import logging
from datetime import timedelta
from django.utils import timezone
from django.db.models import Count, Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.cache import cache

from links.models import NegativeLink

logger = logging.getLogger(__name__)


class DashboardStatsView(APIView):
    """
    API view for dashboard statistics.
    
    GET /api/stats/dashboard/
    
    Returns overall statistics including:
    - Total counts by status
    - New/removed counts for last 7 days
    - Platform-specific statistics
    - Activity chart for last 30 days
    """
    
    def get(self, request):
        """
        Get dashboard statistics with caching.
        """
        # Try to get from cache first
        cache_key = 'dashboard_stats'
        cached_data = cache.get(cache_key)
        
        if cached_data:
            logger.info("Returning cached dashboard stats")
            return Response(cached_data)
        
        logger.info("Calculating dashboard stats")
        
        # Calculate date ranges
        now = timezone.now()
        seven_days_ago = now - timedelta(days=7)
        thirty_days_ago = now - timedelta(days=30)
        
        # Overall statistics
        total = NegativeLink.objects.count()
        active = NegativeLink.objects.filter(status='active').count()
        removed = NegativeLink.objects.filter(status='removed').count()
        in_work = NegativeLink.objects.filter(status='in_work').count()
        pending = NegativeLink.objects.filter(status='pending').count()
        
        # Last 7 days statistics
        new_last_7_days = NegativeLink.objects.filter(
            detected_at__gte=seven_days_ago
        ).count()
        
        removed_last_7_days = NegativeLink.objects.filter(
            removed_at__gte=seven_days_ago,
            removed_at__isnull=False
        ).count()
        
        # Platform statistics
        platforms_data = []
        for platform_code, platform_name in NegativeLink.PLATFORM_CHOICES:
            platform_links = NegativeLink.objects.filter(platform=platform_code)
            
            platform_stats = {
                'platform': platform_code,
                'total': platform_links.count(),
                'active': platform_links.filter(status='active').count(),
                'removed': platform_links.filter(status='removed').count(),
                'in_work': platform_links.filter(status='in_work').count(),
                'new_last_7_days': platform_links.filter(
                    detected_at__gte=seven_days_ago
                ).count()
            }
            
            platforms_data.append(platform_stats)
        
        # Activity chart - last 30 days
        activity_chart = []
        current_date = thirty_days_ago.date()
        end_date = now.date()
        
        while current_date <= end_date:
            next_date = current_date + timedelta(days=1)
            
            active_count = NegativeLink.objects.filter(
                detected_at__date=current_date,
                status='active'
            ).count()
            
            removed_count = NegativeLink.objects.filter(
                removed_at__date=current_date
            ).count()
            
            activity_chart.append({
                'date': current_date.isoformat(),
                'active': active_count,
                'removed': removed_count
            })
            
            current_date = next_date
        
        # Build response
        response_data = {
            'total': total,
            'active': active,
            'removed': removed,
            'in_work': in_work,
            'pending': pending,
            'new_last_7_days': new_last_7_days,
            'removed_last_7_days': removed_last_7_days,
            'platforms': platforms_data,
            'activity_chart': activity_chart
        }
        
        # Cache for 5 minutes
        cache.set(cache_key, response_data, 300)
        
        logger.info("Dashboard stats calculated successfully")
        return Response(response_data)


class PlatformStatsView(APIView):
    """
    API view for platform-specific statistics.
    
    GET /api/stats/platform/{platform}/
    
    Returns statistics for a specific platform.
    """
    
    def get(self, request, platform):
        """
        Get statistics for a specific platform.
        """
        # Validate platform
        valid_platforms = [code for code, _ in NegativeLink.PLATFORM_CHOICES]
        if platform not in valid_platforms:
            return Response(
                {'detail': f'Invalid platform. Must be one of: {", ".join(valid_platforms)}'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Try cache first
        cache_key = f'platform_stats_{platform}'
        cached_data = cache.get(cache_key)
        
        if cached_data:
            logger.info(f"Returning cached stats for platform: {platform}")
            return Response(cached_data)
        
        logger.info(f"Calculating stats for platform: {platform}")
        
        # Calculate date range
        seven_days_ago = timezone.now() - timedelta(days=7)
        
        # Platform statistics
        platform_links = NegativeLink.objects.filter(platform=platform)
        
        platform_stats = {
            'platform': platform,
            'total': platform_links.count(),
            'active': platform_links.filter(status='active').count(),
            'removed': platform_links.filter(status='removed').count(),
            'in_work': platform_links.filter(status='in_work').count(),
            'new_last_7_days': platform_links.filter(
                detected_at__gte=seven_days_ago
            ).count()
        }
        
        # Cache for 5 minutes
        cache.set(cache_key, platform_stats, 300)
        
        logger.info(f"Platform stats calculated for {platform}")
        return Response(platform_stats)
