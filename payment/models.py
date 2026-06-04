from django.conf import settings
from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User


class Payment(models.Model):

    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('SUCCESS', 'Success'),
        ('FAILED', 'Failed')
    ]

    user = models.ForeignKey( settings.AUTH_USER_MODEL,on_delete=models.CASCADE )

    phone_number = models.CharField(  max_length=15 )

    amount = models.DecimalField( max_digits=10,decimal_places=2)

    merchant_request_id = models.CharField( max_length=100,blank=True)

    checkout_request_id = models.CharField( max_length=100, blank=True )

    receipt_number = models.CharField(max_length=100, blank=True)

    status = models.CharField(max_length=20,choices=STATUS_CHOICES,default='PENDING')

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.amount}"

