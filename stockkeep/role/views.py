from rest_framework import generics

from users.permissions import HasPermission
from .models import  Role, RolePermission
from .serializers import  RolePermissionSerializer, RoleSerializer
from drf_yasg.utils import swagger_auto_schema

class ListCreateRole(generics.ListCreateAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer

    @swagger_auto_schema(
        operation_summary="list a role",
        operation_description=""
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary= "create a role",
        operation_description=""
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class RetrieveUpdateDeleteRole(generics.RetrieveUpdateDestroyAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer

class ListCreatePermission(generics.ListCreateAPIView):
    queryset = RolePermission.objects.all()
    serializer_class = RolePermissionSerializer
