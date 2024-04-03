
from rest_framework.views import APIView

from rest_framework.response import Response
from rest_framework import viewsets, status

from Service_Achat.models import BonDeCommande


from .serializers import BonDeReceptionSerializer
from .models import BonDeReception, BonDeReceptionItem




class GenerateReceipt(APIView):
    def post(self, request):
        bon_de_commande_id = request.data.get('bon_de_commande_id', None)
        items_data = request.data.get('items', [])

        if bon_de_commande_id is None:
            return Response({'error': 'Veuillez fournir un identifiant de bon de commande.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            bon_de_commande = BonDeCommande.objects.get(id=bon_de_commande_id)
        except BonDeCommande.DoesNotExist:
            return Response({'error': 'Le bon de commande spécifié n\'existe pas.'}, status=status.HTTP_404_NOT_FOUND)

        bon_de_reception = BonDeReception.objects.create(bon_de_commande=bon_de_commande)

        for item_data in items_data:
            nom_produit = item_data.get('nom_produit')
            print(nom_produit)
            quantite_commandee = item_data.get('quantite_commandee')
            quantite_livree = item_data.get('quantite_livree')
            # Trouver l'objet Item correspondant dans le bon de commande
            items = bon_de_commande.items.filter(produit__designation=nom_produit)
            item = items.first()
            if item:
                # Ajuster la création du BonDeReceptionItem pour utiliser le nom_produit
                BonDeReceptionItem.objects.create(bon_de_reception=bon_de_reception, nom_produit=nom_produit, quantite_commandee=quantite_commandee, quantite_livree=quantite_livree)

        serializer = BonDeReceptionSerializer(bon_de_reception)
        print(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)