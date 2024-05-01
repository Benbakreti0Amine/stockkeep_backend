from rest_framework import generics
from role.models import Role
from users.permissions import HasPermission
from consommateur.models import BonDeCommandeInterne
from .serializers import BonDeCommandeInterneResSerializer
# Create your views here.

class BonDeCommandeInterneRUDView(generics.RetrieveUpdateDestroyAPIView):
    queryset = BonDeCommandeInterne.objects.all()
    serializer_class = BonDeCommandeInterneResSerializer

class BonDeCommandeInterneListView(generics.ListAPIView):
    queryset = BonDeCommandeInterne.objects.all()
    serializer_class = BonDeCommandeInterneResSerializer