
from django.db import models
from django.contrib.auth.models import User 
from datetime import datetime
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import UserManager

CHOICES=(('test1','test1'),('test2','test2'),('test3','test3'),('test4','test4'),)



# Create your models here.
class Profile(models.Model):
	user=models.OneToOneField(User,on_delete=models.CASCADE)
	business_name = models.CharField(max_length=30,blank=True)
	partner_name = models.CharField(max_length=30,blank=True)
	email = models.EmailField(default="@gmail.com")
	phoneNo = models.DecimalField(max_digits=10, decimal_places=0)
	Business_Type = models.CharField(max_length=20,choices=CHOICES,default="test1")
	discount_provided = models.DecimalField(default=0.0,decimal_places=1, max_digits=5)
	Profile_photo = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
	date_joined = models.DateTimeField(default=datetime.now, blank=True)

	objects = models.Manager()

	def save(self, *args, **kwargs):
		user12 = User.objects.filter(username=self.user).update(first_name = self.business_name,email=self.email)
		if self.discount_provided < 0:
			self.discount_provided = 0.0
		super().save(*args, **kwargs)

	class Meta:
		verbose_name_plural = 'Partner Profile'
		verbose_name = 'Partner Profile'


@receiver(post_save,sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender,instance=None,created=False,**kwargs):
	if created:
		Token.objects.create(user=instance)



