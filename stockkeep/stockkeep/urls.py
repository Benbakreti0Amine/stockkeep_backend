"""
URL configuration for stockkeep project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.urls import re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf import settings
from django.conf.urls.static import static


schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('swagger/<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'), 
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'), 
    path('admin/', admin.site.urls),
    path('user/', include('users.urls')),
    path('structure/', include('structure.urls')),
    path('consom/', include('consommateur.urls')),
    path('role/', include('role.urls')),
    path('fournisseur/', include('fournisseur.urls')),
    path('service-achat/', include('Service_Achat.urls')),
    path('magasinier/', include('magasinier.urls')),
    path('responsable/', include('Responsable_structure.urls')),
    path('directeur/', include('directeur.urls')),
    path('notifications/', include('notifications.urls')), # new


]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
