

from rest_framework import serializers
from consommateur.models import BonDeCommandeInterneItem,BonDeCommandeInterne
from Service_Achat.models import Produit


class BonDeCommandeInterneItemSerializer(serializers.ModelSerializer):
    produit = serializers.SlugRelatedField(queryset = Produit.objects.all(), slug_field='designation')
    class Meta:
        model = BonDeCommandeInterneItem
        fields = ['id', 'produit','quantite_demandee','quantite_accorde']

class BonDeCommandeInterneSerializer(serializers.ModelSerializer):
    items = BonDeCommandeInterneItemSerializer(many=True)  # Champ de relation imbriquée

    class Meta:
        model = BonDeCommandeInterne
        fields = ['id', 'Consommateur_id', 'items', 'status', 'date']

    def update(self, instance, validated_data):

        items_data = validated_data.pop('items')
        print(items_data)

        instance = super().update(instance, validated_data)
        instance.status = "Consulted by the responsable"
        for item_data in items_data:
            produit = item_data.get('produit')
            print(produit)
            quantite_accorde = item_data.get('quantite_accorde')
            print(quantite_accorde)
            if produit and quantite_accorde is not None:
                items = instance.items.filter(produit=produit)
                print(items)
                for item in items:
                    item.quantite_accorde = quantite_accorde
                    item.save()
                    
        instance.save()
        return instance    