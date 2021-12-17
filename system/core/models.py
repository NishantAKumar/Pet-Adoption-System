from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import query

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
    accepted_req_id = models.ForeignKey('Request', on_delete=models.CASCADE, blank=True, null=True)
    
    class Meta:
        verbose_name = "Transaction"
        verbose_name_plural = "Transactions"

    def __str__(self):
        return f"{self.donor_id.username}'s {self.name} "

class Request(models.Model):
    transaction_id = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    reason = models.TextField()
    applicant_id = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Request"
        verbose_name_plural = "Requests"

    def __str__(self):
        return f'{self.applicant_id.username} -> {self.transaction_id.donor_id.name}'


class Queries(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    issue = models.TextField(max_length=500)
    phone = models.CharField(max_length=10)
    query = models.TextField()

    class Meta:
        verbose_name = "Query"
        verbose_name_plural = "Queries"

    def __str__(self):
        return self.email


