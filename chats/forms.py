from django.contrib.auth.models import User
from .models import *
from django import forms

class ChatCreate(forms.Form):
	chat_title = forms.CharField(label = "Название чата", max_length = 100)

	class Meta:
		model = Chat
		fields = (
			'__all__'
		)

	def clean(self):
		chat_title = self.cleaned_data["chat_title"]
		return self.cleaned_data

class MessageCreate(forms.Form):
	message_text = forms.CharField(label = "Текст сообщения", max_length = 100)

	class Meta:
		model = Message
		fields = (
			'__all__'
		)

	def clean(self):
		message_text = self.cleaned_data["message_text"]
		return self.cleaned_data