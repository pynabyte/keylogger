from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
from django.utils import timezone
from django.contrib.auth.models import PermissionsMixin
from django.conf import settings

class UserManager(BaseUserManager):
    def create_user(self,email,full_name,password=None,password2=None):
        if not email:
            raise ValueError("The email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email,full_name=full_name)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self,email,full_name, password=None):
        user = self.create_user(email=email, password=password,full_name=full_name)
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)
        return user

REGISTRATION_CHOICES = [
    ('email', 'Email'),
    ('google', 'Google'),
]
class User(AbstractBaseUser,PermissionsMixin):
    email=models.EmailField(verbose_name="Email",max_length=255,unique=True)
    profile_picture = models.ImageField(upload_to="profile_pictures/",null=True,blank=True)
    full_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    objects = UserManager()
    dob = models.DateField(default=timezone.now)
    registration_method = models.CharField(
        max_length=10,
        choices=REGISTRATION_CHOICES,
        default='email'
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["full_name",]

    def __str__(self):
        return self.email

    def has_perm(self,perm,obj=None):
        return self.is_admin

    def has_module_perms(self,app):
        return True # Always true

