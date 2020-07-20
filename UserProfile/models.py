
from django.db import models
from django.contrib.auth.models import User 
from datetime import datetime
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import UserManager

CHOICES=(('a','test1'),('b','test2'),('c','test3'),('d','test4'),)



# Create your models here.
class Profile(models.Model):
	user=models.OneToOneField(User,on_delete=models.CASCADE)
	phoneNo = models.DecimalField(max_digits=10, decimal_places=0)
	Bussiness_Type = models.CharField(max_length=20,choices=CHOICES,default="test1")
	Profile_photo = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
	date_joined = models.DateTimeField(default=datetime.now, blank=True)

	objects = models.Manager()


@receiver(post_save,sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender,instance=None,created=False,**kwargs):
	if created:
		Token.objects.create(user=instance)



