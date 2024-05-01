from rest_framework import serializers

from .models import BonDeReception, BonDeReceptionItem
from .models import BonDeSortie, BonDeSortieItem
from consommateur.models import  BonDeCommandeInterneItem,BonDeCommandeInterne

class BonDeReceptionItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = BonDeReceptionItem
        fields = ['nom_produit', 'quantite_commandee', 'quantite_livree','reste_a_livrer']

class BonDeReceptionSerializer(serializers.ModelSerializer):
    items = BonDeReceptionItemSerializer(many=True, read_only=True)  # Champ de relation imbriquée

    class Meta:
        model = BonDeReception
        fields = ['id', 'bon_de_commande', 'date', 'items']

########################################################################################
###########################################################################################

class BonDeSortieItemSerializer(serializers.ModelSerializer):
    bon_de_commande_interne_item = serializers.PrimaryKeyRelatedField(queryset=BonDeCommandeInterneItem.objects.all())

    class Meta:
        model = BonDeSortieItem
        fields = ['id', 'bon_de_commande_interne_item','observation', 'quantite_accorde']

class BonDeSortieSerializer(serializers.ModelSerializer):
    items = BonDeSortieItemSerializer(many=True)

    class Meta:
        model = BonDeSortie
        fields = ['id', 'bon_de_commande_interne', 'items','type', 'date']
        read_only_fields = ['type']

    def create(self, validated_data):
        id= validated_data.pop('bon_de_commande_interne')
        bon_de_commande_interne_id =id.id
        #print(f"1",bon_de_commande_interne_id)
        bon_de_commande_interne = BonDeCommandeInterne.objects.get(pk=bon_de_commande_interne_id)
        validated_data['type'] = 'Decharge' if bon_de_commande_interne.type == 'Decharge' else 'Supply'
        #print(bon_de_commande_interne)
        bon_de_commande_interne.status = 'Delivered'
        bon_de_commande_interne.save()

        items_data = validated_data.pop('items')
        #print(f"5",items_data)
        bon_de_sortie = BonDeSortie.objects.create(bon_de_commande_interne=bon_de_commande_interne, **validated_data)

        for item_data in items_data:
            bon_de_commande_interne_item = item_data.get('bon_de_commande_interne_item')
            #print(f"14",bon_de_commande_interne_item)
            bon_de_commande_interne_item_id = bon_de_commande_interne_item.id  # Extract identifier
            #print(bon_de_commande_interne_item_id)
            quantite_accorde = item_data.get('quantite_accorde')
            bon_de_commande_interne_item = BonDeCommandeInterneItem.objects.get(pk=bon_de_commande_interne_item_id)
            #print(bon_de_commande_interne_item )
            bon_de_commande_interne_item.quantite_accorde = quantite_accorde
            bon_de_commande_interne_item.save()
            BonDeSortieItem.objects.create(bon_de_sortie=bon_de_sortie, **item_data)


        return bon_de_sortie
    

