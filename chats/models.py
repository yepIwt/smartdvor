from django.db import models
from django.contrib.auth.models import User
import datetime

# Create your models here. Okay.

class Chat(models.Model):
	chat_title = models.CharField("Название чата", max_length = 200)
	members = models.CharField("Участники чата", max_length = 9999, default = "", blank = True) # пиздец, я ведь реально разделяю их как "|"

class Message(models.Model):
	message_author = models.ForeignKey(User, on_delete = models.CASCADE)
	message_text = models.CharField("Текст сообщения", max_length = 200)
	where_locate = models.ForeignKey(Chat, on_delete = models.CASCADE)
	when = models.DateField('Дата отправки', null=True, blank=True, default = datetime.date.today)