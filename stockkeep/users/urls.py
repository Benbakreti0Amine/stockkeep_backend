from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
urlpatterns = [
    path('listcreate/',views.ListCreateUser.as_view(), name='listcreate'),
    path('rud/<int:pk>/',views.RetrieveUpdateDeleteUser.as_view(), name='RetrieveUpdateDelete'),
    path('active/<int:user_id>/',views.Activate_OR_Desactivate.as_view(), name='active'),
    path("jwt/create/", TokenObtainPairView.as_view(), name="jwt_create"),
    path("jwt/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("jwt/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("login/", views.LoginView.as_view(), name="login"),

]