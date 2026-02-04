from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Industry, Template
from .serializers import IndustrySerializer, TemplateSerializer

class IndustryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API to list all industries.
    """
    queryset = Industry.objects.all()
    serializer_class = IndustrySerializer

class TemplateViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API to list templates.
    Supports filtering by industry via query param ?industry_id=X
    """
    queryset = Template.objects.all()
    serializer_class = TemplateSerializer

    def get_queryset(self):
        queryset = Template.objects.all()
        industry_id = self.request.query_params.get('industry_id')
        if industry_id:
            queryset = queryset.filter(industry_id=industry_id)
        return queryset
