
from rest_framework import generics,status
from rest_framework.views import APIView
from users.permissions import HasPermission
from .models import  Role, RolePermission
from .serializers import  RolePermissionSerializer, RoleSerializer
from rest_framework.response import Response

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

class GetPermOfRole(APIView):

   def post(self, request):
        role_name = request.data.get('name', None)
        if role_name:
            try:
                role = Role.objects.get(name=role_name)
                print(role)
                role_permissions = role.rolepermission_set.all() #retrieves all related RolePermission instances associated with the role.
                print(role_permissions)
                permissions = [rp.auth_permission for rp in role_permissions] 
                print(permissions)
                permission_data = [{'id': perm.id, 'name': perm.name, 'codename': perm.codename} for perm in permissions]
                return Response({'role': role_name, 'permissions': permission_data})
            except Role.DoesNotExist:
                return Response({'error': f'Role with name {role_name} does not exist'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'error': 'Role name not provided'}, status=status.HTTP_400_BAD_REQUEST)