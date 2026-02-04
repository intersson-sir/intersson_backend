from rest_framework import serializers
from .models import DiscussProject

class DiscussProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiscussProject
        fields = '__all__'
        read_only_fields = ('created_at',)
