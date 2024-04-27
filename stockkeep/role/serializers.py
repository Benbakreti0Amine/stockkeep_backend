from rest_framework import serializers
from .models import  Role, RolePermission
from django.contrib.auth.models import Permission
class RoleSerializer(serializers.ModelSerializer):
    

    class Meta:
        model = Role
        fields = ['name', 'id']

class RolePermissionSerializer(serializers.ModelSerializer):
    role = serializers.SlugRelatedField(queryset = Role.objects.all(), slug_field='name')
    auth_permission = serializers.SlugRelatedField(queryset = Permission.objects.all(), slug_field='codename',)
    

    class Meta:
        model = RolePermission
        fields = ['id', 'role','auth_permission']

