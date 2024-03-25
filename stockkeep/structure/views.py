
from rest_framework import generics
from rest_framework.exceptions import ValidationError
from users.permissions import HasPermission
from .models import Structure
from .serializers import StructureSerializer




class ListCreateStructure(generics.ListCreateAPIView):
    queryset = Structure.objects.all()
    serializer_class = StructureSerializer

class RetrieveUpdateDeleteStructure(generics.RetrieveUpdateDestroyAPIView):
    queryset = Structure.objects.all()
    serializer_class = StructureSerializer

#verification if this role has user related with it
    def destroy(self, request, *args, **kwargs):
            instance = self.get_object()

            print(instance)
            
            # Check if the instance has any related objects
            if instance.consommateur_set.exists():
                # Customize this message according to your requirements
                error_message = "Cannot delete this object because it has related objects."
                raise ValidationError(error_message)

            return super().destroy(request, *args, **kwargs)

