from rest_framework import serializers

from .models import Notification
from role.models import Role


class NotificationSerializer(serializers.ModelSerializer):
    role = serializers.SlugRelatedField(queryset = Role.objects.all(), slug_field='name')
    class Meta:
        model = Notification
        fields = '__all__'

class Notification2Serializer(serializers.Serializer):
    title = serializers.CharField(max_length=100)
    body = serializers.CharField(max_length=255)
    data = serializers.JSONField(required=False) 
