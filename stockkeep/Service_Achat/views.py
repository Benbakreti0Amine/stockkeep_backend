
from rest_framework import generics

from .models import Article, BonDeCommande ,Chapitre, Produit
from .serializers import BonDeCommandeSerializer, ChapitreSerializer, ProduitSerializer, articleSerializer,ItemSerializer

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

    def perform_destroy(self, instance):
        # Delete associated products if any
        produits = instance.produits.all()
        for produit in produits:
            if not produit.articles.exists():
                produit.delete()
        # Call the superclass' perform_destroy to delete the article
        super().perform_destroy(instance)

class ListCreateProduit(generics.ListCreateAPIView):
    queryset = Produit.objects.all()
    serializer_class = ProduitSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        quantite_en_security = serializer.validated_data.get('quantite_en_security')
        quantite_en_stock = serializer.validated_data.get('quantite_en_stock')
        print(quantite_en_security)
        
        if quantite_en_security > quantite_en_stock:       
            return Response({"error": "Quantity in security cannot be greater than quantity in stock."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

            


        
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
