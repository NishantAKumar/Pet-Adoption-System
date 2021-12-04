from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    area = models.CharField(max_length=500)
    city = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    phone = models.CharField(max_length=10)
   
class Transaction(models.Model):

    name=models.CharField(max_length=100)
    desc= models.TextField()
    img = models.ImageField(upload_to='pics')
    donor_id = models.ForeignKey(User, on_delete=models.CASCADE)
    accepted_req_id = models.ForeignKey('Request', on_delete=models.CASCADE, blank=True)


class Request(models.Model):
    transaction_id = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    reason = models.TextField()
    applicant_id = models.ForeignKey(User, on_delete=models.CASCADE)

