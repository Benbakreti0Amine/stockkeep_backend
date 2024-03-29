from rest_framework import serializers
from .models import Article, BonDeCommande, Chapitre, Item, Produit

class ChapitreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chapitre
        fields = '__all__'

class articleSerializer(serializers.ModelSerializer):
    chapitre = serializers.SlugRelatedField(queryset = Chapitre.objects.all(), slug_field='libelle')
    class Meta:
        model = Article
        fields = ['id','designation','chapitre']

class ProduitSerializer(serializers.ModelSerializer):
    article = serializers.SlugRelatedField(queryset = Article.objects.all(), slug_field='designation')
    class Meta:
        model = Produit
        fields = ['id','designation','article']


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['id', 'chapitre', 'article', 'produit', 'prix_unitaire', 'quantite', 'montant']

    # def create(self, validated_data):
    #     # Calculate montant based on prix_unitaire and quantite
    #     prix_unitaire = validated_data.get('prix_unitaire')
    #     quantite = validated_data.get('quantite')
    #     validated_data['montant'] = prix_unitaire * quantite
    #     return super().create(validated_data)

class BonDeCommandeSerializer(serializers.ModelSerializer):
    items = ItemSerializer(many=True)  # Nested serializer for Item

    class Meta:
        model = BonDeCommande
        fields = ['id', 'fournisseur', 'items', 'tva', 'montant_global', 'date', 'status']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        bon_de_commande = BonDeCommande.objects.create(**validated_data)
        for item_data in items_data:
            Item.objects.create(bon_de_commande=bon_de_commande, **item_data)
        return bon_de_commande
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['items'] = ItemSerializer(instance.items.all(), many=True).data
        return representation