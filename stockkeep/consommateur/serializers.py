from role.models import Role
from structure.models import Structure
from rest_framework import serializers
from .models import Consommateur

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
    

