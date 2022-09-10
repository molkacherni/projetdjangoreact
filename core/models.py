from pyexpat import model
from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils import timezone
import uuid 

from .managers import CustomUserManager

def upload_to(instance, filename):
    return 'user_profile_image/{}/{}'.format(instance.user.id, filename)
# Create your models here.
class User(AbstractBaseUser, PermissionsMixin):
    
    # These fields tie to the roles!
    SUPERADMIN = 1
    RH = 2
    EMPLOYEE = 3

    ROLE_CHOICES = (
        (SUPERADMIN, 'Super-Admin'),
        (RH, 'Rh'),
        (EMPLOYEE, 'Employee')
    )
    
    class Meta:
        app_label = 'core' 
        verbose_name = 'core'
        verbose_name_plural = 'cores'

    uid = models.UUIDField(unique=True, editable=False, default=uuid.uuid4, verbose_name='Public identifier')
    email = models.EmailField(unique=True,blank=True)
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, blank=True, null=True, default=3)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True ,blank=True, null=True)
    is_staff = models.BooleanField(default=False ,blank=True, null=True)
    is_superuser = models.BooleanField(default=False ,blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    created_date = models.DateTimeField(default=timezone.now)
    modified_date = models.DateTimeField(default=timezone.now)
    created_by = models.EmailField()
    modified_by = models.EmailField()

    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

class ProfileUser(models.Model):
    GENDER = (
        ('M', 'Homme'),
        ('F', 'Femme'),
    )
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    registration_number = models.CharField(max_length=50, blank=True)
    phone_number = models.CharField(max_length=50, blank=True)
    address = models.CharField(max_length=200, blank=True)
    post = models.CharField(max_length=100, blank=True)
    image = models.ImageField(blank=True, upload_to=upload_to, null=True)
    birthday=models.DateField(auto_now=False, null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER)

    def __str__(self):
        return self.post
