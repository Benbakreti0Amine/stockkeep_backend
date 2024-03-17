from django.db import models

class Structure(models.Model):
    name = models.CharField(max_length=100,unique=True)
    abbreviation = models.CharField(max_length=10,unique=True)
    responsible = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
    


