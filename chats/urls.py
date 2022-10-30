from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.conf import settings
from django.urls import path
from . import views

app_name = 'chats'

urlpatterns = [
	path("", views.list_chats, name = 'list_chats'),
	path("create/", views.create_chat, name = "create_chat"),
	path("<int:pk>/", views.chat_view, name = "chat_view"),
	path("<int:pk>/in/", views.add_user_to_chat, name = "add_user_to_chat"),
]
