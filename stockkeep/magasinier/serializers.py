from rest_framework import serializers

from .models import BonDeReception, BonDeReceptionItem
from .models import BonDeSortie, BonDeSortieItem
from consommateur.models import  BonDeCommandeInterneItem

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
        fields = ['id', 'bon_de_commande_interne', 'items', 'date']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        print(items_data)
        bon_de_sortie = BonDeSortie.objects.create(**validated_data)

        for item_data in items_data:
            BonDeSortieItem.objects.create(bon_de_sortie=bon_de_sortie, **item_data)

        return bon_de_sortie