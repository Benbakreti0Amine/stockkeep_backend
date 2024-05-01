from django.urls import path
from . import views


urlpatterns = [   
    path('bondereception/list/',views.BonDeReceptionListView.as_view(), name='listreceipt'),
    path('bondereception/rud/<int:pk>/',views.BonDeReceptionRUDView.as_view(), name='deletereceipt'),
    path('bondereception/create/', views.GenerateReceipt.as_view(), name='generate_receipt'),
    path('bondereception/<int:bon_de_reception_id>/pdf/', views.GeneratePDFView.as_view(), name='generate_pdf'),
    path('bondesortie/create/', views.BonDeSortieCreateView.as_view(), name='genererbondesortie'),
    path('bondesortie/list/', views.BonDeSortieListView.as_view(), name='genererbondesortie'),
    path('bondecommandeinterne/list/',views.BonDeCommandeInterneListView.as_view(), name='bonlist'),
] 