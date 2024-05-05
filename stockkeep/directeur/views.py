
from rest_framework import generics
from consommateur.models import BonDeCommandeInterne
from magasinier.models import EtatInventaire
from .serializers import BonDeCommandeInterneDicSerializer,EtatInventaireDirSerializer
# Create your views here.

class BonDeCommandeInterneRUDView(generics.RetrieveUpdateDestroyAPIView):
    queryset = BonDeCommandeInterne.objects.all()
    serializer_class = BonDeCommandeInterneDicSerializer

class BonDeCommandeInterneListView(generics.ListAPIView):
    queryset = BonDeCommandeInterne.objects.all()
    serializer_class = BonDeCommandeInterneDicSerializer


class EtatInventaireDirListView(generics.ListAPIView):
    queryset = EtatInventaire.objects.all()
    serializer_class = EtatInventaireDirSerializer

class EtatInventaireDirRUDView(generics.RetrieveUpdateDestroyAPIView):
    queryset = EtatInventaire.objects.all()
    serializer_class = EtatInventaireDirSerializer