from django.urls import path
from . import views


urlpatterns = [   
    path('bondereception/list/',views.BonDeReceptionListView.as_view(), name='listreceipt'),
    path('bondereception/rud/<int:pk>/',views.BonDeReceptionRUDView.as_view(), name='deletereceipt'),
    path('bondereception/create/', views.GenerateReceipt.as_view(), name='generate_receipt'),
] 