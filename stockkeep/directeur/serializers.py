from role.models import Role
from structure.models import Structure
from rest_framework import serializers
from consommateur.models import Consommateur,BonDeCommandeInterneItem,BonDeCommandeInterne
from users.models import User
from Service_Achat.models import Produit

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
        instance.status = "directeur"
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