from django.db import models
from users.models import User
from structure.models import Structure
# Create your models here.
from django.contrib.auth.models import  BaseUserManager

class MyUserManager(BaseUserManager): 
     def create_user(self, username, email,first_name,last_name, password, **kwags):
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have a username')
        if not first_name:
            raise ValueError('Users must have a firstname')
        if not last_name:
            raise ValueError('Users must have a lastname')

        user = self.model(
            username=username,
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name
        )
        user.is_active  = True
        user.set_password(password)
        user.save(using=self._db)
        return user
     

class Consommateur(User):
    structure = models.ForeignKey(Structure,on_delete=models.SET_NULL,null=True)
    objects = MyUserManager()

   