
from rest_framework import generics

from users.permissions import HasPermission
from .models import  Role, RolePermission
from .serializers import  RolePermissionSerializer, RoleSerializer


class ListCreateRole(generics.ListCreateAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [HasPermission]

class RetrieveUpdateDeleteRole(generics.RetrieveUpdateDestroyAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [HasPermission]

class ListCreatePermission(generics.ListCreateAPIView):
    queryset = RolePermission.objects.all()
    serializer_class = RolePermissionSerializer