from rest_framework import serializers
from .models import Structure
from users.models import User

class StructureSerializer(serializers.ModelSerializer):
    responsible = serializers.SlugRelatedField(queryset=User.objects.filter(role__name='responsable_structure'), slug_field='username')

    class Meta:
        model = Structure
        fields = ['name', 'id','abbreviation', 'responsible']


    




