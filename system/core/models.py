from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    area = models.CharField(max_length=500)
    city = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    phone = models.CharField(max_length=10)
    
    
class Transaction(models.Model): # Follow the models.field format
    # I've done the basic thing because I had to verify my part works
    donor_id = models.ForeignKey(User, on_delete=models.CASCADE)
    # id:int
    # donor_id:int
    # img: str
    # desc:str
    # fk_Rid: int


class Request(models.Model):
    transaction_id = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    reason = models.TextField()
    applicant_id = models.ForeignKey(User, on_delete=models.CASCADE)
