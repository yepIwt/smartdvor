from urllib.parse import parse_qsl
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.urls import reverse


from core.models import Profile, Service
from core.forms import RegistrationForm, CompleteRegistrationForm, LoginForm, ServiceForm

# Create your views here. Okay.

def all_users(request):

	all = User.objects.all()
	return render(request, 'users/list.html', {'users': all})

def registration(request):

	form = RegistrationForm(request.POST or None)
	if request.POST and form.is_valid():
		username = form.cleaned_data['username']
		email = form.cleaned_data['email']
		password = form.cleaned_data['password']

		user = User.objects.create_user(username, email, password)
		login(request, user)

		prof = User.objects.get(username__exact = request.user)
		prof.save()

		return HttpResponseRedirect(reverse("frontend:complete"))
	return render(request,'users/register.html',{'form':form})

def complete_registration(request):

	form = CompleteRegistrationForm(request.POST or None)
	if request.POST and form.is_valid():
		prof = User.objects.get(username__exact = request.user)
		prof.profile.sex = form.cleaned_data['sex']
		prof.profile.address = form.cleaned_data['address']
		prof.profile.bthd = form.cleaned_data['bthd']
		prof.save()
		return HttpResponseRedirect(reverse("frontend:user", args = [prof.username]))
	return render(request,'users/r_complete.html',{'form':form})

def user(request, username):

	try:
		user = User.objects.get(username__exact = username)
	except:
		return HttpResponse('<h1>Такого пользователя не существует</h1>')

	contex = {'usr': user}
	return render(request,'users/page.html',contex)

def login_page(request):

	form = LoginForm(request.POST or None); err = False
	if request.POST and form.is_valid():
		username = form.cleaned_data['username']
		password = form.cleaned_data['password']

		user = authenticate(request=request, username = username, password = password)
		if user is not None:
			login(request, user)
			return HttpResponseRedirect(reverse("frontend:user", args = [user.username]))
		else:
			err = True
	return render(request,'users/login_page.html',{'form':form, 'err': err})

def logout_page(request):
	logout(request)
	return HttpResponseRedirect(reverse("frontend:all_users"))

def user_requests(request, username):
	
	try:
		u = User.objects.get(username__exact = request.user)
	except:
		raise HttpResponse("<h1>Авторизуйтесь</h1>")

	requests = u.service_set.order_by('-id')
	print(requests)
	
	form = ServiceForm(request.POST or None)
	if request.POST and form.is_valid():

		comment = form.cleaned_data['comment']
		serivice_type = form.cleaned_data['serivice_type']

		r = Service(customer = u, serivice_type = serivice_type, comment = comment)
		r.save()

	return render(request, "requests/my.html", {"form": form, 'requests': requests})