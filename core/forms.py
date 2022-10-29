from django.contrib.auth.models import User
from .models import Profile
from django import forms
import datetime

class RegistrationForm(forms.Form):

	username =  forms.CharField(widget=forms.TextInput(), required=True)
	email = forms.EmailField(required=True)
	password = forms.CharField(widget=forms.PasswordInput())
	password2 = forms.CharField(widget=forms.PasswordInput())

	class Meta:
		model = User
		fields = (
			'__all__'
		)

	def clean(self):
		
		username = self.cleaned_data["username"]
		email = self.cleaned_data["email"]
		password = self.cleaned_data["password"]
		password2 = self.cleaned_data["password2"]

		if password != password2:
			raise forms.ValidationError("Пароли не совпадают.")

		# Check user exist
		email_taken = User.objects.filter(email=email)

		if email_taken:
			raise forms.ValidationError({'email':["Такая почта уже существует."]})
		
		# Check username exist
		username_taken = User.objects.filter(username = username)
		if username_taken:
			raise forms.ValidationError({'username':["Такой ник уже существует."]})

		if password:
			if len(password) < 5:
				raise forms.ValidationError("Пароль слишком простой (не менее 5 символов).")

		return self.cleaned_data

class DateInput(forms.DateInput):
	input_type = 'date'

class CompleteRegistrationForm(forms.Form):
	#username = forms.CharField(label="Имя пользователя", max_length =100)
	address = forms.CharField(label="Адрес", max_length=100)
	bthd = forms.DateField(widget = DateInput)

	sex_choice = (
		(True, 'Мужчина'),
		(False,'Женщина')
	)

	sex = forms.ChoiceField(choices = sex_choice)

	class Meta:
		model = Profile
		widgets = {'bthd' : DateInput() }
		fields = (
			'__all__'
		)

	def clean(self):
		#username = self.cleaned_data['username']
		address = self.cleaned_data['address']
		bthd = self.cleaned_data['bthd']
		sex = self.cleaned_data['sex']

		if bthd > datetime.date.today():
			raise forms.ValidationError('Неправильная дата рождения')

		if datetime.date.today().year - bthd.year - ((datetime.date.today().month, datetime.date.today().day) < (bthd.month, bthd.day)) <=14:
			raise forms.ValidationError('Вход только с 15')

		return self.cleaned_data

class LoginForm(forms.Form):
	username = forms.CharField(label="Имя пользователя", max_length =100)
	password = forms.CharField(widget=forms.PasswordInput())
	class Meta:
		model = User
		fields = (
			'__all__'
		)
	
	def clean(self):
		username = self.cleaned_data['username']
		password = self.cleaned_data['password']

		# Check username exist
		username_taken = User.objects.filter(username = username)
		if not username_taken:
			raise forms.ValidationError({'username':["Такого ника нет."]})
		
		return self.cleaned_data