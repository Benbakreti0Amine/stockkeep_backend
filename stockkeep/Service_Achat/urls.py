from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter
from .views import ItemViewSet

router = DefaultRouter()
router.register(r'bondecommande/(?P<bon_de_commande_id>\d+)/items', ItemViewSet, basename='item')

urlpatterns = [
    path('Produit/listcreate/',views.ListCreateProduit.as_view(), name='listcreateProduit'),
    path('Produit/rud/<int:pk>/',views.RetrieveUpdateDeleteProduit.as_view(), name='deleteProduit'),
    path('Article/listcreate/',views.ListCreatearticle.as_view(), name='listcreateArticle'),
    path('Article/rud/<int:pk>/',views.RetrieveUpdateDeletearticle.as_view(), name='deleteArticle'),    
    path('Chapitre/listcreate/',views.ListCreateChapitre.as_view(), name='listcreateChapitre'),
    path('Chapitre/rud/<int:pk>/',views.RetrieveUpdateDeleteChapitre.as_view(), name='deleteChapitre'),
    path('bondecommande/listcreate/',views.BonDeCommandeCreateView.as_view(), name='bondecommande'),
    path('bondecommande/rud/<int:pk>/',views.BonDeCommandeRUDView.as_view(), name='bondecommandeid'),
    path('bondecommande/<int:bon_de_commande_id>/pdf/', views.GeneratePDFView.as_view(), name='generate_pdf'),
    path('Article/<int:article_id>/Produits/', views.ArticleProduitsAPIView.as_view(), name='article-produits'),
    path('Chapitre/<int:chapitre_id>/Articles/', views.ChapitreArticlesAPIView.as_view(), name='chapitre-articles'),
    path('Chapitre/<int:chapitre_id>/Produits/', views.ChapitreProduitsAPIView.as_view(), name='chapitre-produits'),
] + router.urls
