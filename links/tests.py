"""
Tests for links app (placeholder).
"""
from django.test import TestCase
from django.utils import timezone
from .models import NegativeLink


class NegativeLinkModelTest(TestCase):
    """
    Test cases for NegativeLink model.
    """
    
    def setUp(self):
        """Set up test data."""
        self.link = NegativeLink.objects.create(
            url='https://example.com/negative-post',
            platform='facebook',
            type='post',
            status='active',
            priority='high'
        )
    
    def test_link_creation(self):
        """Test that a link can be created."""
        self.assertIsNotNone(self.link.id)
        self.assertEqual(self.link.platform, 'facebook')
        self.assertEqual(self.link.status, 'active')
    
    def test_removed_at_auto_set(self):
        """Test that removed_at is set when status changes to removed."""
        self.link.status = 'removed'
        self.link.save()
        self.assertIsNotNone(self.link.removed_at)
    
    def test_string_representation(self):
        """Test string representation."""
        expected = f"facebook - post (active)"
        self.assertEqual(str(self.link), expected)
