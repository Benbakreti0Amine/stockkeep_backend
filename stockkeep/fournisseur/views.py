
from rest_framework import generics

from .models import Fournisseur
from .serializers import FournisseurSerializer


class ListCreateFournisseur(generics.ListCreateAPIView):
    queryset = Fournisseur.objects.all()
    serializer_class = FournisseurSerializer
class RetrieveUpdateDeleteFournisseur(generics.RetrieveUpdateDestroyAPIView):
    queryset = Fournisseur.objects.all()
    serializer_class = FournisseurSerializer
