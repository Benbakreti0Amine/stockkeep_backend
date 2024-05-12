
from rest_framework import generics
from consommateur.models import BonDeCommandeInterne
from directeur.models import TicketSuiviCommande
from .serializers import BonDeCommandeInterneDicSerializer, TicketSuiviCommandeSerializer
# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView

class BonDeCommandeInterneRUDView(generics.RetrieveUpdateDestroyAPIView):
    queryset = BonDeCommandeInterne.objects.all()
    serializer_class = BonDeCommandeInterneDicSerializer

class BonDeCommandeInterneListView(generics.ListAPIView):
    queryset = BonDeCommandeInterne.objects.all()
    serializer_class = BonDeCommandeInterneDicSerializer

class TicketListView(generics.ListAPIView):
    queryset = TicketSuiviCommande.objects.all()
    serializer_class = TicketSuiviCommandeSerializer

# class TicketSearchView(APIView):
#     def get(self, request, bon_de_commande_id):
#         tickets = TicketSuiviCommande.objects.filter(bon_de_commande_id=bon_de_commande_id)
#         serializer = TicketSuiviCommandeSerializer(tickets, many=True)
#         return Response(serializer.data)
    
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