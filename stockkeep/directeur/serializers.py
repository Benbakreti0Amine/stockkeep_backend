from role.models import Role
from directeur.models import TicketSuiviCommande
from structure.models import Structure
from rest_framework import serializers
from consommateur.models import Consommateur,BonDeCommandeInterneItem,BonDeCommandeInterne
from magasinier.models import EtatInventaireProduit,EtatInventaire
from users.models import User
from Service_Achat.models import Produit,Chapitre,Article

from rest_framework.validators import ValidationError

class UserSerializer(serializers.ModelSerializer):
    structure = serializers.SlugRelatedField(queryset = Structure.objects.all(), slug_field='name')
    role = serializers.SlugRelatedField(read_only=True, slug_field='name')

    


    class Meta:
        model = Consommateur
        fields = ['id', 'username','password', 'email', 'first_name', 'last_name', 'is_active','structure','role']
        ref_name = 'ConsommateurUser'

    def to_representation(self,instance):
        rep = super(UserSerializer,self).to_representation(instance)
        rep['structure']=instance.structure.name
        # rep['role']=instance.role.name
        return rep
    
    def validate(self, attrs):
     email = attrs.get("email")  # Use get() method to safely retrieve email field

     if email:
        email_exists = User.objects.filter(email=email).exists()
        if email_exists:
            raise ValidationError("Email has already been used")

     return super().validate(attrs)


    def create(self, validated_data):
        password = validated_data.pop("password")

        user = super().create(validated_data)

        user.set_password(password)

        user.save()


        return user
    

class BonDeCommandeInterneItemDicSerializer(serializers.ModelSerializer):
    produit = serializers.SlugRelatedField(queryset = Produit.objects.all(), slug_field='designation')
    class Meta:
        model = BonDeCommandeInterneItem
        fields = ['id', 'produit','quantite_demandee','quantite_accorde']

class BonDeCommandeInterneDicSerializer(serializers.ModelSerializer):
    items = BonDeCommandeInterneItemDicSerializer(many=True)  # Champ de relation imbriquée

    class Meta:
        model = BonDeCommandeInterne
        fields = ['id', 'user_id', 'items', 'status','type', 'date']

    def update(self, instance, validated_data):

        items_data = validated_data.pop('items')
        print(items_data)
        instance = super().update(instance, validated_data)
        instance.status = "Consulted by the director"
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
        TicketSuiviCommande.create_ticket(bon_de_commande=instance, etape='directeur', items_info=items_info) 
        instance.save()
        return instance    
    


class EtatInventaireDicProduitSerializer(serializers.ModelSerializer):
    produit = serializers.SlugRelatedField(queryset = Produit.objects.all(), slug_field="designation")

    class Meta:
        model = EtatInventaireProduit
        fields = ['produit', 'quantite_physique', 'observation','N_inventaire']

class EtatInventaireDirSerializer(serializers.ModelSerializer):
    chapitre = serializers.SlugRelatedField(queryset=Chapitre.objects.all(), slug_field="libelle")
    article = serializers.SlugRelatedField(queryset=Article.objects.all(), slug_field="designation")
    produits = EtatInventaireDicProduitSerializer(many=True)

    class Meta:
        model = EtatInventaire
        fields = ['id', 'datetime', 'chapitre', 'article', 'etat', 'produits']


    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        instance.etat = "Approuved"
        instance.save()

        produits_data = instance.produits.all()
        for produit_data in produits_data:
            produit_id = produit_data.id
            quantite_physique = produit_data.quantite_physique
            produit = instance.produits.get(id=produit_id).produit
            produit.quantite_en_stock = quantite_physique
            produit.save()

        return instance
    

class TicketSuiviCommandeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketSuiviCommande
        fields = ['bon_de_commande', 'etape', 'items']