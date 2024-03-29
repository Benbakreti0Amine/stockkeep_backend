from django.urls import path
from . import views

urlpatterns = [
    path('Produit/listcreate/',views.ListCreateProduit.as_view(), name='listcreateProduit'),
    path('Produit/rud/<int:pk>/',views.RetrieveUpdateDeleteProduit.as_view(), name='deleteProduit'),
    path('Article/listcreate/',views.ListCreatearticle.as_view(), name='listcreateArticle'),
    path('Article/rud/<int:pk>/',views.RetrieveUpdateDeletearticle.as_view(), name='deleteArticle'),    
    path('Chapitre/listcreate/',views.ListCreateChapitre.as_view(), name='listcreateChapitre'),
    path('Chapitre/rud/<int:pk>/',views.RetrieveUpdateDeleteChapitre.as_view(), name='deleteChapitre'),
    path('bondecommande/',views.BonDeCommandeCreateView.as_view(), name='bondecommande'),
]