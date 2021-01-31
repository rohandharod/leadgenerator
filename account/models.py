from django.db import models
from django.conf import settings
# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    role =  models.CharField(max_length=20)
    phone = models.CharField(max_length=10)
    alt_phone = models.CharField(max_length=10)
    designation = models.CharField(max_length=50)
    address = models.TextField()
    mapped_to = models.CharField(max_length=50)
    mapped_to_name = models.CharField(max_length=10)
    by_online = models.CharField(max_length=3)

class Leads(models.Model):
    lead_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=25)
    phone = models.CharField(max_length=10)
    alt_phone = models.CharField(max_length=10)
    email = models.CharField(max_length=50)
    reference = models.CharField(max_length=50)
    product = models.CharField(max_length=50)
    loan_amt = models.CharField(max_length=10)
    address = models.TextField()
    pincode = models.CharField(max_length=6)
    country = models.CharField(max_length=25)
    state = models.CharField(max_length=25)
    city = models.CharField(max_length=25) 
    added_by = models.CharField( max_length=50)

