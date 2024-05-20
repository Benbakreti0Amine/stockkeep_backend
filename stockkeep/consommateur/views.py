
from rest_framework import generics
from role.models import Role
from .models import Consommateur,BonDeCommandeInterne
from .serializers import UserSerializer,BonDeCommandeInterneSerializer
from django.contrib.auth.models import  BaseUserManager
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import BonDeCommandeInterne, Consommateur
from datetime import datetime
import calendar

# Create your views here.



class ListCreateCons(generics.ListCreateAPIView):

    queryset = Consommateur.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        print (serializer.validated_data)
        name = serializer.validated_data.get('username')
        role = serializer.validated_data.get('role') or None
        if role is None:
            role = 'consommateur'
        # Retrieve the corresponding Role instance from the database
        role_instance, _ = Role.objects.get_or_create(name=role)
        serializer.save(role=role_instance)
    



class RetrieveUpdateDeleteCons(generics.RetrieveUpdateDestroyAPIView):
    queryset = Consommateur.objects.all()
    serializer_class = UserSerializer
    
class BonDeCommandeInterneCreateView(generics.ListCreateAPIView):
    queryset = BonDeCommandeInterne.objects.all()
    serializer_class = BonDeCommandeInterneSerializer
    
class BonDeCommandeInterneRUDView(generics.RetrieveUpdateDestroyAPIView):
    queryset = BonDeCommandeInterne.objects.all()
    serializer_class = BonDeCommandeInterneSerializer


def bci_statistics_for_consommateur(request, id):
    # Get the consommateur object or return 404 if not found
    consommateur = get_object_or_404(Consommateur, id=id)

    # Query BCIs for the specified consommateur
    bc_interne = BonDeCommandeInterne.objects.filter(Consommateur_id=consommateur)

    # Prepare a dictionary to hold the statistics
    stats = {}

    for bci in bc_interne:
        # Extract the month and year from the date
        month_year = bci.date.strftime('%Y-%m')
        month_name = bci.date.strftime('%B')

        if month_year not in stats:
            stats[month_year] = {
                'month_name': month_name,
                'count': 0
            }

        stats[month_year]['count'] += 1

    # Convert stats dictionary to a list of dictionaries for JSON response
    monthly_data = []
    for month_year, data in stats.items():
        monthly_data.append({
            'month_year': month_year,
            'month_name': data['month_name'],
            'count': data['count']
        })

    response_data = {
        'consommateur_id': consommateur.id,
        'name': consommateur.username,
        'monthly_data': monthly_data
    }

    return JsonResponse(response_data, safe=False)