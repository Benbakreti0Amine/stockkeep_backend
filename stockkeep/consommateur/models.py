from django.db import models
from users.models import User
from structure.models import Structure
# Create your models here.

class Consommateur(User):
    structure = models.ForeignKey(Structure,on_delete=models.SET_NULL,null=True)

    
