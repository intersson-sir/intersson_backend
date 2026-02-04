from rest_framework import viewsets, mixins
from .models import Review
from .serializers import ReviewSerializer

class ReviewViewSet(mixins.CreateModelMixin,
                    mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    viewsets.GenericViewSet):
    """
    API for submitting reviews and listing approved reviews.
    """
    serializer_class = ReviewSerializer

    def get_queryset(self):
        # Only show approved reviews to the public
        # For Create, it doesn't matter as we return the instance (usually), 
        # but standard is to return the created instance.
        # If we strictly want to hide unapproved, we could adjust logic, but default is fine.
        # List action: Filter by approved.
        return Review.objects.filter(is_approved=True)
