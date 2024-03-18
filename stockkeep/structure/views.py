
from rest_framework import generics

from users.permissions import HasPermission
from .models import Structure
from .serializers import StructureSerializer


class ListCreateStructure(generics.ListCreateAPIView):
    queryset = Structure.objects.all()
    serializer_class = StructureSerializer
    permission_classes = [HasPermission]

class RetrieveUpdateDeleteStructure(generics.RetrieveUpdateDestroyAPIView):
    queryset = Structure.objects.all()
    serializer_class = StructureSerializer

