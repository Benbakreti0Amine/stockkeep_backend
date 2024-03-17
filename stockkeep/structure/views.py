
from rest_framework import generics
from .models import Structure
from .serializers import StructureSerializer


class ListCreateStructure(generics.ListCreateAPIView):
    queryset = Structure.objects.all()
    serializer_class = StructureSerializer

class RetrieveUpdateDeleteStructure(generics.RetrieveUpdateDestroyAPIView):
    queryset = Structure.objects.all()
    serializer_class = StructureSerializer

