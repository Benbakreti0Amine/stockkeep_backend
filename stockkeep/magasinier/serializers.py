from rest_framework import serializers

from Service_Achat.models import Produit

from .models import BonDeReception, BonDeReceptionItem
from .models import BonDeSortie, BonDeSortieItem,EtatInventaireProduit,EtatInventaire#,FicheMovement
from consommateur.models import  BonDeCommandeInterneItem,BonDeCommandeInterne
from consommateur.serializers import  BonDeCommandeInterneItemSerializer

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
    

class BonDeCommandeInterneMagaSerializer(serializers.ModelSerializer):
    items = BonDeCommandeInterneItemSerializer(many=True)  # Nested relationship field

    class Meta:
        model = BonDeCommandeInterne
        fields = ['id', 'Consommateur_id', 'items', 'status','type', 'date']
        read_only_fields = ['status']  # Mark status field as read-only

    def create(self, validated_data):
        items_data = validated_data.pop('items')

        validated_data['status'] = 'External Discharge'  

        bon_de_commande = BonDeCommandeInterne.objects.create(**validated_data)

        for item_data in items_data:
            produit_designation = item_data.pop('produit')
            produit = Produit.objects.get(designation=produit_designation)
            item_data['produit'] = produit

            item_serializer = BonDeCommandeInterneItemSerializer(data=item_data)
            if item_serializer.is_valid():
                item = item_serializer.save()
                bon_de_commande.items.add(item)
        
        bon_de_commande.save()

        return bon_de_commande
    
######################################################################
##################################################################
class EtatInventaireProduitSerializer(serializers.ModelSerializer):
    produit = serializers.SlugRelatedField(queryset=Produit.objects.all(), slug_field="designation")

    class Meta:
        model = EtatInventaireProduit
        fields = ['produit', 'quantite_physique', 'quantite_logique', 'observation']
        read_only = ['quantite_logique']

class EtatInventaireSerializer(serializers.ModelSerializer):
    produits = EtatInventaireProduitSerializer(many=True)

    class Meta:
        model = EtatInventaire
        fields = ['id','datetime', 'etat', 'produits']
        read_only_fields = ['etat']

    def create(self, validated_data):

        produits_data = validated_data.pop('produits')

        validated_data['etat'] = 'Not Approuved' 

        etat_inventaire_produits = []

        for produit_data in produits_data:
            produit = produit_data.pop('produit')
            quantite_physique = produit_data.pop('quantite_physique')
            observation = produit_data.pop('observation')

            if produit.quantite_en_stock <= 0:
                raise serializers.ValidationError("The product {} has no stock available.".format(produit.designation))

            # Check if the product is already associated with the EtatInventaire
            if EtatInventaireProduit.objects.filter(produit=produit, quantite_physique=quantite_physique).exists():
                raise serializers.ValidationError("An entry for product {} with the same name already exists in this inventory state.".format(produit.designation))
            quantite_logique = produit.quantite_en_stock
            produit.quantite_en_stock = quantite_physique
            produit.save()
            etat_inventaire_produit = EtatInventaireProduit.objects.create(produit=produit, quantite_physique=quantite_physique, observation=observation,quantite_logique=quantite_logique)
            etat_inventaire_produits.append(etat_inventaire_produit)

        etat_inventaire = EtatInventaire.objects.create()
        
        # Add associated produits using set()
        etat_inventaire.produits.set(etat_inventaire_produits)
        
        return etat_inventaire
    
    def update(self, instance, validated_data):
        produits_data = validated_data.pop('produits')

        # Update existing EtatInventaireProduit instances and add new ones
        for produit_data in produits_data:
            produit = produit_data.get('produit')
            quantite_physique = produit_data.get('quantite_physique')
            observation = produit_data.get('observation')
            
            if produit and quantite_physique is not None:

                # Update existing instance or create new one
                etat_inventaire_produit, created = EtatInventaireProduit.objects.get_or_create(
                    produit=produit,
                    defaults={'quantite_physique': quantite_physique, 'observation': observation}
                )
                if not created:
                    # If the instance already existed, update its fields
                    etat_inventaire_produit.quantite_physique = quantite_physique
                    etat_inventaire_produit.observation = observation
                    etat_inventaire_produit.save()
                    produit.quantite_en_stock = quantite_physique
                    produit.save()
                instance.produits.add(etat_inventaire_produit)

                # Update the quantite_en_stock of the product
                produit.quantite_en_stock = quantite_physique
                produit.save()

        instance.save()
        return instance


# class FicheMovementSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = FicheMovement
#         fields = '__all__'

#     def get_read_only_fields(self, *args, **kwargs):
#         read_only_fields = super().get_read_only_fields(*args, **kwargs)
#         read_only_fields.extend(['date_entree', 'fournisseur', 'quantite_entree', 'consommateur', 'date_sortie', 'quantite_sortie', 'numero_bon', 'reste', 'observations'])
#         return read_only_fields