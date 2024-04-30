
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView

from rest_framework.response import Response
from rest_framework import viewsets, status

from Service_Achat.models import BonDeCommande
from Service_Achat.serializers import BonDeCommandeSerializer

from Service_Achat.serializers import BonDeCommandeSerializer
from consommateur.models import BonDeCommandeInterne, BonDeCommandeInterneItem
from .serializers import BonDeReceptionSerializer, BonDeSortieItemSerializer, BonDeSortieSerializer
from .models import BonDeReception, BonDeReceptionItem
from rest_framework import generics

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
        
        bon_de_reception_count = BonDeReception.objects.filter(bon_de_commande=bon_de_commande).count()
        bon_de_reception = BonDeReception.objects.create(bon_de_commande=bon_de_commande)
        
        print(bon_de_reception_count)

        for item_data in items_data:
            nom_produit = item_data.get('nom_produit')
            print(nom_produit)
            quantite_livree = item_data.get('quantite_livree')
            items = bon_de_commande.items.filter(produit__designation=nom_produit)
            item = items.first()
            print(items)
            if item:
                # Check if it's the first reception for this product
                reception = BonDeReceptionItem.objects.filter(nom_produit=nom_produit)
                print(reception)
                first_reception = bon_de_reception_count == 0

                if first_reception:
                    quantite_commandee = item.quantite # No previous orders
                else:
                    # Retrieve the most recent BonDeReceptionItem and get its reste_a_livrer value
                    last_reception_item = reception.order_by('-id').first()
                    quantite_commandee = last_reception_item.reste_a_livrer

                BonDeReceptionItem.objects.create(bon_de_reception=bon_de_reception, nom_produit=nom_produit, quantite_commandee=quantite_commandee, quantite_livree=quantite_livree)

        serializer = BonDeReceptionSerializer(bon_de_reception)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

class BonDeReceptionListView(generics.ListAPIView):
    queryset = BonDeReception.objects.all()
    serializer_class = BonDeReceptionSerializer
    
class BonDeReceptionRUDView(generics.RetrieveUpdateDestroyAPIView):
    queryset = BonDeReception.objects.all()
    serializer_class = BonDeReceptionSerializer

    ############################################
    ############################################


# class BonDeSortieCreateView(APIView):
#     def post(self, request, *args, **kwargs):
#         bon_de_commande_interne_id = request.data.get('bon_de_commande_interne_id')
#         observation = request.data.get('observation', '')
#         items_data = request.data.get('items', [])

#         # Implement your logic to validate bon_de_commande_interne_id and items_data

#         bon_de_sortie_data = {
#             'bon_de_commande_interne': bon_de_commande_interne_id,
#             'observation': observation,
#             'items': items_data
#         }

#         serializer = BonDeSortieSerializer(data=bon_de_sortie_data)
#         if serializer.is_valid():
#             bon_de_sortie = serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BonDeSortieCreateView(APIView):
    def post(self, request, *args, **kwargs):
        bon_de_commande_interne_id = request.data.get('bon_de_commande_interne_id')
        items_data = request.data.get('items', [])

        bon_de_commande_interne = get_object_or_404(BonDeCommandeInterne, pk=bon_de_commande_interne_id)


        bon_de_sortie_data = {
            'bon_de_commande_interne': bon_de_commande_interne_id,
            'items': []
        }

        for item_data in items_data:
            bon_de_commande_interne_item_id = item_data.get('bon_de_commande_interne_item')
            quantite_accorde = item_data.get('quantite_accorde')
            observation_item = item_data.get('observation_item', '')

            # Retrieve the BonDeCommandeInterneItem instance
            print(bon_de_commande_interne_item_id)
            bon_de_commande_interne_item = get_object_or_404(BonDeCommandeInterneItem, pk=bon_de_commande_interne_item_id)
            print('11111111111111111111111111113333333333333')
 
            # Create the item data for BonDeSortie
            item_serializer = BonDeSortieItemSerializer(data={
                'bon_de_commande_interne_item': bon_de_commande_interne_item_id,
                'quantite_accorde': quantite_accorde,
                'observation': observation_item
            })
            print(item_serializer.is_valid())
            print('//////////////////////////yy')
            print(bon_de_commande_interne_item_id)
            print(quantite_accorde)
            print(item_serializer)


            if item_serializer.is_valid():
                bon_de_sortie_data['items'].append(item_serializer.validated_data)
                print('/////////////////////////')
                print(item_serializer.validated_data)
            else:
                return Response(item_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        print('/////////////////////////')
        serializer = BonDeSortieSerializer(data=bon_de_sortie_data)
        print('123')
        print(bon_de_sortie_data)
        print('/////////////////////////////////////////')
        print('123')
        print(serializer.is_valid())
        print('/////////////////////////////////////////')
        print(serializer.data)


        if serializer.is_valid():      
            print(serializer.data)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)