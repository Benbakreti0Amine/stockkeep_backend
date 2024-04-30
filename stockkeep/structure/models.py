from django.db import models
from users.models import User

class Structure(models.Model):
    name = models.CharField(max_length=100,unique=True)
    abbreviation = models.CharField(max_length=10,unique=True)
    responsible = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role__name': 'responsable_structure'},related_name="resposable",null=True)

    def __str__(self):
        return self.name
    
    


