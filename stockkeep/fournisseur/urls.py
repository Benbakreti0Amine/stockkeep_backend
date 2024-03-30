from django.urls import path
from . import views

urlpatterns = [
    path('listcreate/',views.ListCreateFournisseur.as_view(), name='listcreatefournisseur'),
    path('rud/<int:pk>/',views.RetrieveUpdateDeleteFournisseur.as_view(), name='deletefournisseur'),
]