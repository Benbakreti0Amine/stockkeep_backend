from rest_framework import serializers

from .models import Notification
from role.models import Role


class NotificationSerializer(serializers.ModelSerializer):
    role = serializers.SlugRelatedField(queryset = Role.objects.all(), slug_field='name')
    class Meta:
        model = Notification
        fields = '__all__'