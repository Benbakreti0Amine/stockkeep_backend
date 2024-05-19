
from rest_framework import generics
from consommateur.models import BonDeCommandeInterne
from magasinier.models import EtatInventaire
from directeur.models import TicketSuiviCommande
from .serializers import BonDeCommandeInterneDicSerializer,EtatInventaireDirSerializer, TicketSuiviCommandeSerializer
from rest_framework.response import Response
from rest_framework.views import APIView

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

class TicketListView(generics.ListAPIView):
    queryset = TicketSuiviCommande.objects.all()
    serializer_class = TicketSuiviCommandeSerializer


    
class TicketSearchView(APIView):
    def get(self, request, bon_de_commande_id):
        tickets = TicketSuiviCommande.objects.filter(bon_de_commande_id=bon_de_commande_id)
        data = {
            "bon_de_commande": bon_de_commande_id,
            "etapes": []
        }
        for ticket in tickets:
            data["etapes"].append({
                "etape": ticket.etape,
                "items": ticket.items
            })
        return Response(data) 