from django.db import models
from django.contrib.auth.models import User
import datetime
from django.db.models.signals import post_save

from django.dispatch import receiver

# Create your models here. Okay.

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
	sex = models.BooleanField('Пол человека', default=False) #False - Девушка. True - Парень
	address = models.CharField('Адрес', max_length = 100, blank=True, null=True)
	bthd = models.DateField('Дата рождения', null=True, blank=True)

	def __str__(self):
		return str(self.user.username)
	
	def age(self):
		date = self.bthd
		return datetime.date.today().year - date.year - ((datetime.date.today().month, datetime.date.today().day) < (date.month, date.day))

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
	if created:
		Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
	instance.profile.save()