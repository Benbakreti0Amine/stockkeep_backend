from rest_framework import generics
from django.contrib.auth.models import Permission
from .serializers import PermissionSerializer

class PermissionList(generics.ListCreateAPIView):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
