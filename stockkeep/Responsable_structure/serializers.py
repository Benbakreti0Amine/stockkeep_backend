

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

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        bon_de_commande = BonDeCommandeInterne.objects.create(**validated_data)

        for item_data in items_data:

            produit_designation = item_data.pop('produit')

            produit = Produit.objects.get(designation=produit_designation)



            item_data['produit'] = produit

            item_serializer = BonDeCommandeInterneItemSerializer(data=item_data)
            if item_serializer.is_valid():
                item = item_serializer.save()
                bon_de_commande.items.add(item)
            else:
                # Handle serializer errors
                pass


        bon_de_commande.save()

        return bon_de_commande
    


    def update(self, instance, validated_data):

        items_data = validated_data.pop('items')
        print(items_data)

        instance = super().update(instance, validated_data)
        instance.status = "responsable"
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

