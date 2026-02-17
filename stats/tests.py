"""
Tests for stats app (placeholder).
"""
from django.test import TestCase
from rest_framework.test import APIClient
from links.models import NegativeLink


class StatsAPITest(TestCase):
    """
    Test cases for stats API endpoints.
    """
    
    def setUp(self):
        """Set up test client and data."""
        self.client = APIClient()
        
        # Create test data
        NegativeLink.objects.create(
            url='https://example.com/post1',
            platform='facebook',
            type='post',
            status='active'
        )
        NegativeLink.objects.create(
            url='https://example.com/post2',
            platform='twitter',
            type='comment',
            status='removed'
        )
    
    def test_dashboard_stats(self):
        """Test dashboard stats endpoint."""
        response = self.client.get('/api/stats/dashboard/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('total', response.data)
        self.assertEqual(response.data['total'], 2)
    
    def test_platform_stats(self):
        """Test platform stats endpoint."""
        response = self.client.get('/api/stats/platform/facebook/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('platform', response.data)
        self.assertEqual(response.data['platform'], 'facebook')
