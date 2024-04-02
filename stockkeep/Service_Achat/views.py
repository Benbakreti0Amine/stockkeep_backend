
from rest_framework import generics

from .models import Article, BonDeCommande, BonDeReception, BonDeReceptionItem, Chapitre, Item, Produit
from .serializers import BonDeCommandeSerializer, BonDeReceptionItemSerializer, BonDeReceptionSerializer, ChapitreSerializer, ProduitSerializer, articleSerializer,ItemSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets, status

class ListCreateChapitre(generics.ListCreateAPIView):
    queryset = Chapitre.objects.all()
    serializer_class = ChapitreSerializer
class RetrieveUpdateDeleteChapitre(generics.RetrieveUpdateDestroyAPIView):
    queryset = Chapitre.objects.all()
    serializer_class = ChapitreSerializer

class ListCreatearticle(generics.ListCreateAPIView):
    queryset = Article.objects.all()
    serializer_class = articleSerializer
class RetrieveUpdateDeletearticle(generics.RetrieveUpdateDestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = articleSerializer

class ListCreateProduit(generics.ListCreateAPIView):
    queryset = Produit.objects.all()
    serializer_class = ProduitSerializer
class RetrieveUpdateDeleteProduit(generics.RetrieveUpdateDestroyAPIView):
    queryset = Produit.objects.all()
    serializer_class = ProduitSerializer



    
class BonDeCommandeCreateView(generics.ListCreateAPIView):
    queryset = BonDeCommande.objects.all()
    serializer_class = BonDeCommandeSerializer
    
class BonDeCommandeRUDView(generics.RetrieveUpdateDestroyAPIView):
    queryset = BonDeCommande.objects.all()
    serializer_class = BonDeCommandeSerializer


from decimal import Decimal

class ItemViewSet(viewsets.ViewSet):
    def create(self, request, bon_de_commande_id):
        bon_de_commande = BonDeCommande.objects.get(pk=bon_de_commande_id)
        serializer = ItemSerializer(data=request.data)
        if serializer.is_valid():
            item = serializer.save()
            bon_de_commande.items.add(item)
            
            # Recalculate montant_global
            bon_de_commande.montant_global = sum(item.montant for item in bon_de_commande.items.all())
            bon_de_commande.save()
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
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