
from rest_framework import generics

from .models import Article, BonDeCommande, Chapitre, Item, Produit
from .serializers import BonDeCommandeSerializer, ChapitreSerializer, ProduitSerializer, articleSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
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

    def perform_create(self, serializer):
        # Save the BonDeCommande instance to get an ID
        bon_de_commande_instance = serializer.save()
        
        # Now add related Item instances
        items_data = self.request.data.get('items', [])
        for item_data in items_data:
            item_data['bon_de_commande'] = bon_de_commande_instance.id
            Item.objects.create(**item_data)
    