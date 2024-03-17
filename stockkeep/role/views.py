
from rest_framework import generics
from .models import Role
from .serializers import RoleSerializer


class ListCreateRole(generics.ListCreateAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer

class RetrieveUpdateDeleteRole(generics.RetrieveUpdateDestroyAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer

