from rest_framework.permissions import BasePermission
from django.contrib.auth.models import Permission

from role.models import RolePermission


def _permission(request, view) -> bool:
    """
    Dynamically extracts permission from Django Role
    """
    if not request.user.is_authenticated:
        return False
    if request.user.is_superuser:
        return True
    
    action_type = ''
    if request.method == 'GET':
        action_type = 'view'
    elif request.method == 'POST':
        action_type = 'add'
    elif request.method == 'PUT' or request.method == 'PATCH':
        action_type = 'change'
    elif request.method == 'DELETE':
        action_type = 'delete'
    
    
    # Force evaluation of queryset to get the model
    model = view.queryset.model

    
    codename = f'{action_type}_{model.__name__.lower()}'
    print(codename)
    print(request.user.role)

   
    return RolePermission.objects.filter(
        auth_permission__codename=codename,
        role=request.user.role
    ).exists()

                      

class HasPermission(BasePermission):

    def has_permission(self, request, view):
        """
        Checks View Permission
        """
        return _permission(request, view)
                                                            
    def has_object_permission(self, request, view, obj):
        """
        Checks Object Permission
        """
        return _permission(request, view)