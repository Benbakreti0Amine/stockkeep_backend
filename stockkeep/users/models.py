from django.db import models

# Create your models here.
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

from role.models import Role

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
            last_name=last_name,
        )

        user.is_active  = True
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email,first_name,last_name, password):
        user = self.create_user(username=username,email=email, password=password,first_name=first_name,last_name=last_name)


        user.is_staff = True
        role = user.role
        if role is None:
            role = 'admin'
        # Retrieve the corresponding Role instance from the database
        role_instance, _ = Role.objects.get_or_create(name=role)
        user.is_superuser = True
        user.role=role_instance
        user.save()

class User(AbstractBaseUser, PermissionsMixin):

    alphanumeric = RegexValidator(r'^[0-9a-zA-Z]*$', message='Only alphanumeric characters are allowed.')
    username    = models.CharField(unique=True, max_length=20, validators=[alphanumeric])
    email       = models.EmailField(verbose_name='email address', unique=True, max_length=244)
    first_name  = models.CharField(max_length=30, null=True, blank=True)
    last_name   = models.CharField(max_length=50, null=True, blank=True)
    is_active   = models.BooleanField(default=True, null=False)
    is_staff    = models.BooleanField(default=False, null=False)
    role = models.ForeignKey(Role,on_delete=models.SET_NULL,null=True,default='consommateur')


   

    objects = MyUserManager()

    USERNAME_FIELD  = 'email'
    REQUIRED_FIELDS = ['username','last_name','first_name']

    def get_full_name(self):
        fullname = self.first_name+" "+self.last_name
        return self.fullname

    def get_short_name(self):
        return self.username

    def str(self):
        return self.email

