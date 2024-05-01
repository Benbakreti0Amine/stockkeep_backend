
from rest_framework import generics
from consommateur.models import BonDeCommandeInterne
from .serializers import BonDeCommandeInterneDicSerializer
# Create your views here.

class BonDeCommandeInterneRUDView(generics.RetrieveUpdateDestroyAPIView):
    queryset = BonDeCommandeInterne.objects.all()
    serializer_class = BonDeCommandeInterneDicSerializer

class BonDeCommandeInterneListView(generics.ListAPIView):
    queryset = BonDeCommandeInterne.objects.all()
    serializer_class = BonDeCommandeInterneDicSerializer