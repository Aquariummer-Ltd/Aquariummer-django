from rest_framework import serializers

from core.models import Fish


class FishSerializer(serializers.ModelSerializer):
    """Serializer for fish object"""

    class Meta:
        model = Fish
        fields = ('id', 'name')
        read_only_fields = ('id',)
