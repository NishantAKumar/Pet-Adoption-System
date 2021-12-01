from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    area = models.CharField(max_length=500)
    city = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    phone = models.CharField(max_length=10)
