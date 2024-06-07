

from rest_framework import serializers
from consommateur.models import BonDeCommandeInterneItem,BonDeCommandeInterne
from Service_Achat.models import Produit
from directeur.models import TicketSuiviCommande


class BonDeCommandeInterneItemResSerializer(serializers.ModelSerializer):
    produit = serializers.SlugRelatedField(queryset = Produit.objects.all(), slug_field='designation')
    class Meta:
        model = BonDeCommandeInterneItem
        fields = ['id', 'produit','quantite_demandee','quantite_accorde']
  

class BonDeCommandeInterneResSerializer(serializers.ModelSerializer):
    items = BonDeCommandeInterneItemResSerializer(many=True)  # Champ de relation imbriquée

    class Meta:
        model = BonDeCommandeInterne
        fields = ['id', 'user_id', 'items', 'status', 'type', 'date']

    def update(self, instance, validated_data):
        items_data = validated_data.pop('items')
        print(items_data)

        # Update the status before calling super().update()
        instance.status = "Validated by the responsable"

        # Perform the update and set status without saving immediately
        instance = super().update(instance, validated_data)

        # Update the related items
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

        items_info = [{'item': item.produit.designation, 'quantite': item.quantite_accorde} for item in instance.items.all()]
        TicketSuiviCommande.create_ticket(bon_de_commande=instance, etape='responsable', items_info=items_info)

        # Save the instance only once after all changes
        instance.save()

        return instance
