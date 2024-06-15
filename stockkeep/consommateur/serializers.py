from role.models import Role
from directeur.models import TicketSuiviCommande
from structure.models import Structure
from rest_framework import serializers
from .models import Consommateur,BonDeCommandeInterneItem,BonDeCommandeInterne
from users.models import User
from Service_Achat.models import Produit
from directeur.models import TicketSuiviCommande
from rest_framework.validators import ValidationError

class UserSerializer(serializers.ModelSerializer):
    structure = serializers.SlugRelatedField(queryset = Structure.objects.all(), slug_field='name')
    role = serializers.SlugRelatedField(read_only=True, slug_field='name')

    


    class Meta:
        model = Consommateur
        fields = ['id', 'username','password', 'email', 'first_name', 'last_name', 'is_active','structure','role','image','token']
        ref_name = 'ConsommateurUser'

    def to_representation(self,instance):
        rep = super(UserSerializer,self).to_representation(instance)
        rep['structure']=instance.structure.name
        return rep
    
    def validate(self, attrs):
     email = attrs.get("email") 

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
    

class BonDeCommandeInterneItemSerializer(serializers.ModelSerializer):
    produit = serializers.SlugRelatedField(queryset = Produit.objects.all(), slug_field='designation')
    class Meta:
        model = BonDeCommandeInterneItem
        fields = ['id', 'produit','quantite_demandee','quantite_accorde']

class BonDeCommandeInterneSerializer(serializers.ModelSerializer):
    items = BonDeCommandeInterneItemSerializer(many=True)  

    class Meta:
        model = BonDeCommandeInterne
        fields = ['id', 'user_id', 'items', 'status','type', 'date']
        read_only_fields = ['status'] 

    def create(self, validated_data):
        items_data = validated_data.pop('items')

        validated_data['status'] = 'Created succesfully'  

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
        items_info = [{'item': item['produit'].designation, 'quantite': item['quantite_demandee']} for item in items_data]
        
        TicketSuiviCommande.objects.create(bon_de_commande=bon_de_commande, etape='consommateur', items=items_info)
        return bon_de_commande


    def update(self, instance, validated_data):
        items_data = validated_data.pop('items', [])  

        instance = super().update(instance, validated_data)

        for item_data in items_data:
            produit = item_data.get('produit')
            quantite_demandee = item_data.get('quantite_demandee')

            if produit and quantite_demandee is not None:

                item, created = instance.items.get_or_create(produit=produit, defaults={'quantite_demandee': 0})


                item.quantite_demandee = quantite_demandee
                item.save()

        return instance   