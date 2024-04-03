from django.urls import path
from . import views


urlpatterns = [   
    # path('bondereception/list/',views.ListCreateChapitre.as_view(), name='listcreateChapitre'),
    # path('bondereception/rud/<int:pk>/',views.RetrieveUpdateDeleteChapitre.as_view(), name='deleteChapitre'),
    path('bondereception/create/', views.GenerateReceipt.as_view(), name='generate_receipt'),
] 