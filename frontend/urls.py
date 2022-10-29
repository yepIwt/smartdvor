from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.conf import settings
from django.urls import path
from . import views

app_name = 'frontend'

urlpatterns = [
	path('all/', views.all_users, name = 'all_users'),
	path('r/', views.registration, name = 'registration'),
	path('r/comp/', views.complete_registration, name = 'complete'),
	path('l/', views.login_page, name = "login_page"),
	path('logout/', views.logout_page, name='logout_page'),
	path('<str:username>', views.user, name='user'),
]
