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

class Post(models.Model):
	post_title = models.CharField("Название поста", max_length = 200)
	post_text = models.TextField("Текст поста")
	pub_date = models.DateField("Дата создания поста", default = datetime.date.today)
	post_author = models.ForeignKey(User, on_delete = models.CASCADE)

	def __str__(self):
		return f"{self.post_author.username}: '{self.post_title}'"

class PostComment(models.Model):
	post = models.ForeignKey(Post, on_delete = models.CASCADE)
	comment_author = models.ForeignKey(User, on_delete = models.CASCADE)
	comment_text = models.CharField("Текст комментария", max_length = 200)

	def __str__(self):
		return f"{self.comment_author.username}: {self.post.post_title} - {self.comment_text}"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
	if created:
		Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
	instance.profile.save()