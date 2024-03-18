from django.db import models
from django.contrib.auth.models import Permission

class Role(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class RolePermission(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    auth_permission = models.ForeignKey(Permission, on_delete=models.CASCADE)

    # def __str__(self):
    #     return f"{self.role.name} - {self.auth_permission.name}"
