from django.shortcuts import get_object_or_404, render
from rest_framework import generics
from role.models import Role
from .models import Consommateur
from structure.models import Structure
from .serializers import UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
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
    
