from rest_framework import viewsets, mixins
from .models import DiscussProject
from .serializers import DiscussProjectSerializer

class DiscussProjectViewSet(mixins.CreateModelMixin,
                            viewsets.GenericViewSet):
    """
    API endpoint that allows project inquiries to be submitted.
    """
    queryset = DiscussProject.objects.all()
    serializer_class = DiscussProjectSerializer
