from rest_framework import serializers
from .models import Industry, Template

class TemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Template
        fields = ['id', 'title', 'pdf_file', 'hero_image', 'industry', 'created_at']

class IndustrySerializer(serializers.ModelSerializer):
    # Optional: include templates if needed, but requirements say "Get templates by industry"
    class Meta:
        model = Industry
        fields = ['id', 'name']
