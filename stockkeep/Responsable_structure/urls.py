from django.urls import path
from . import views


urlpatterns = [
    path('bondecommandeinterne/rud/<int:pk>/',views.BonDeCommandeInterneRUDView.as_view(), name='bon-rud'),

]