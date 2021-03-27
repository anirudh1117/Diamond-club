from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.

class AllCoupon(models.Model):
    card_Number = models.PositiveIntegerField(blank=False)
    card_valid = models.DateField(blank=False)
    card_user_id = models.PositiveIntegerField(blank=False)
    card_user_name = models.CharField(max_length=30,blank=True)
 
    def __str__(self):
        return f'{self.card_Number}' 


class CouponHistory(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)  
    card_number =  models.PositiveIntegerField(blank=False)
    partner_name = models.CharField(max_length=30,blank=True)
    scannedAt = models.DateTimeField(default=datetime.now, blank=True) 

    class Meta:
        verbose_name_plural = 'Scanned History'
        verbose_name = 'Scanned History'