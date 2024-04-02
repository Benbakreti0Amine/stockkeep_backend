from rest_framework import serializers
from .models import Article, BonDeCommande, BonDeReception, BonDeReceptionItem, Chapitre, Item, Produit

class ChapitreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chapitre
        fields = '__all__'

class articleSerializer(serializers.ModelSerializer):
    chapitre = serializers.SlugRelatedField(queryset = Chapitre.objects.all(), slug_field='libelle')
    class Meta:
        model = Article
        fields = ['designation','chapitre','tva']

class ProduitSerializer(serializers.ModelSerializer):
    article = serializers.SlugRelatedField(queryset = Article.objects.all(), slug_field='designation')
    class Meta:
        model = Produit
        fields = ['designation','article']


class ItemSerializer(serializers.ModelSerializer):
    chapitre = serializers.SlugRelatedField(queryset = Chapitre.objects.all(), slug_field='libelle')
    article = serializers.SlugRelatedField(queryset = Article.objects.all(), slug_field='designation')
    produit = serializers.SlugRelatedField(queryset = Produit.objects.all(), slug_field='designation')
    class Meta:
        model = Item
        fields = ['id','chapitre', 'article', 'produit', 'prix_unitaire', 'quantite', 'montant']

class BonDeCommandeSerializer(serializers.ModelSerializer):
    items = ItemSerializer(many=True)

    class Meta:
        model = BonDeCommande
        fields = ['id','fournisseur', 'items', 'tva', 'montant_global', 'date', 'status']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        bon_de_commande = BonDeCommande.objects.create(**validated_data)

        for item_data in items_data:
            chapitre_libelle = item_data.pop('chapitre')
            article_designation = item_data.pop('article')
            produit_designation = item_data.pop('produit')

            chapitre = Chapitre.objects.get(libelle=chapitre_libelle)
            article = Article.objects.get(designation=article_designation, chapitre=chapitre)
            produit = Produit.objects.get(designation=produit_designation, article=article)


            item_data['chapitre'] = chapitre
            item_data['article'] = article
            item_data['produit'] = produit

            item_serializer = ItemSerializer(data=item_data)
            if item_serializer.is_valid():
                item = item_serializer.save()
                bon_de_commande.items.add(item)
            else:
                # Handle serializer errors
                pass

        if bon_de_commande.items.exists():
            bon_de_commande.tva = bon_de_commande.items.first().article.tva

        montant_global = sum(item.prix_unitaire * item.quantite for item in bon_de_commande.items.all())
        bon_de_commande.montant_global = montant_global
        bon_de_commande.save()

        return bon_de_commande

class BonDeReceptionItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = BonDeReceptionItem
        fields = ['nom_produit', 'quantite_commandee', 'quantite_livree','reste_a_livrer']

class BonDeReceptionSerializer(serializers.ModelSerializer):
    items = BonDeReceptionItemSerializer(many=True, read_only=True)  # Champ de relation imbriquée

    class Meta:
        model = BonDeReception
        fields = ['id', 'bon_de_commande', 'date', 'items']





# class ItemReceivedSerializer(serializers.ModelSerializer):
#     item = ItemSerializer()
#     class Meta:
#         model = ItemReceived
#         fields = ['id','item','quantite_livree','reste_a_livrer']
    
    

# class BonDeReceptionSerializer(serializers.ModelSerializer):
#     # bon_de_commande = BonDeCommandeSerializer()
#     bon_de_commande = serializers.SlugRelatedField(queryset = Chapitre.objects.all(), slug_field='id')
#     class Meta:
#         model = BonDeCommande
#         fields = ['id','bon_de_commande']

#     def create(self, validated_data):
#         items_data = validated_data.pop('items')
        



# def update(self, instance, validated_data):
#         items_data = validated_data.pop('items')
#         instance.fournisseur = validated_data.get('fournisseur', instance.fournisseur)
#         instance.tva = validated_data.get('tva', instance.tva)
#         instance.date = validated_data.get('date', instance.date)
#         instance.status = validated_data.get('status', instance.status)
        
        
#         instance.items.clear()
#         # Update or create items
#         for item_data in items_data:
#             item_id = item_data.get('id', None)
#             if item_id:
#                 item = Item.objects.get(id=item_id)
#                 chapitre_libelle = item_data['chapitre'].libelle
#                 article_designation = item_data['article'].designation
#                 produit_designation = item_data['produit'].designation


#                 item.chapitre = Chapitre.objects.get(libelle=chapitre_libelle)
#                 item.article = Article.objects.get(designation=article_designation, chapitre=item.chapitre)
#                 item.produit = Produit.objects.get(designation=produit_designation, article=item.article)
#                 item.prix_unitaire = item_data.get('prix_unitaire', item.prix_unitaire)
#                 item.quantite = item_data.get('quantite', item.quantite)
#                 item.montant = item_data.get('montant', item.montant)
#                 item.save()
#                 instance.items.add(item)
#             else:
#                 chapitre_libelle = item_data['chapitre'].libelle
#                 article_designation = item_data['article'].designation
#                 produit_designation = item_data['produit'].designation


#                 item5 = Item.objects.create(
#                     chapitre=Chapitre.objects.get(libelle=chapitre_libelle),
#                     article=Article.objects.get(designation=article_designation),
#                     produit=Produit.objects.get(designation=produit_designation),
#                     prix_unitaire=item_data.get('prix_unitaire'),
#                     quantite=item_data.get('quantite'),
#                 )
#                 instance.items.add(item5)  

#         # Calculate tva based on the first item's associated article's tva
#         if instance.items.exists():
#             instance.tva = instance.items.first().article.tva

#         # Recalculate montant_global
#         montant_global = sum(item.prix_unitaire * item.quantite for item in instance.items.all())
#         instance.montant_global = montant_global
#         instance.save()

#         print("\nUpdated montant_global:", instance.montant_global)

#         return instance