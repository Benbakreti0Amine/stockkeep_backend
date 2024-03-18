from rest_framework.permissions import BasePermission
from django.contrib.auth.models import Permission


def _permission(request, view) -> bool:
    """
    Dynamically extracts permission from Django Role
    """



    action_type = ''
    if request.method == 'GET':
        action_type = 'view'
    elif request.method == 'POST':
        action_type = 'add'
    elif request.method == 'PUT' or request.method == 'PATCH':
        action_type = 'change'
    elif request.method == 'DELETE':
        action_type = 'delete'
    
    print("1 "+ action_type)
    model = view.queryset.model.__name__
    print(model)
    codename=f'{action_type}_{model.lower()}'
    print(codename)
    return Permission.objects.filter(
        codename=codename,
        user__username=request.user.username
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