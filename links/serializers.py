"""
Serializers for the links app.
"""
from rest_framework import serializers
from .models import NegativeLink


class NegativeLinkSerializer(serializers.ModelSerializer):
    """
    Serializer for NegativeLink model.
    Handles conversion between NegativeLink instances and JSON.
    """
    
    class Meta:
        model = NegativeLink
        fields = [
            'id',
            'url',
            'platform',
            'type',
            'status',
            'detected_at',
            'removed_at',
            'priority',
            'manager',
            'notes',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'detected_at', 'created_at', 'updated_at']
    
    def validate_url(self, value):
        """
        Validate URL field.
        """
        if not value or not value.strip():
            raise serializers.ValidationError("URL cannot be empty.")
        return value.strip()
    
    def update(self, instance, validated_data):
        """
        Update instance with special handling for status changes.
        When status changes to 'removed', removed_at is set automatically in the model.
        """
        return super().update(instance, validated_data)


class BulkUpdateStatusSerializer(serializers.Serializer):
    """
    Serializer for bulk status update operation.
    """
    ids = serializers.ListField(
        child=serializers.UUIDField(),
        min_length=1,
        help_text="List of link IDs to update"
    )
    status = serializers.ChoiceField(
        choices=NegativeLink.STATUS_CHOICES,
        help_text="New status to set"
    )
    
    def validate_ids(self, value):
        """Validate that all IDs exist."""
        if not value:
            raise serializers.ValidationError("At least one ID is required.")
        return value


class BulkAssignManagerSerializer(serializers.Serializer):
    """
    Serializer for bulk manager assignment operation.
    """
    ids = serializers.ListField(
        child=serializers.UUIDField(),
        min_length=1,
        help_text="List of link IDs to update"
    )
    manager = serializers.CharField(
        max_length=100,
        help_text="Manager name to assign"
    )
    
    def validate_ids(self, value):
        """Validate that all IDs exist."""
        if not value:
            raise serializers.ValidationError("At least one ID is required.")
        return value
    
    def validate_manager(self, value):
        """Validate manager name."""
        if not value or not value.strip():
            raise serializers.ValidationError("Manager name cannot be empty.")
        return value.strip()
