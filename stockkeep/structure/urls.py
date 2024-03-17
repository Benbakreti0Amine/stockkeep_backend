from django.urls import path
from . import views

urlpatterns = [
    path('listcreate/',views.ListCreateStructure.as_view(), name='listcreate'),
    path('rud/<int:pk>/',views.RetrieveUpdateDeleteStructure.as_view(), name='delete'),
]