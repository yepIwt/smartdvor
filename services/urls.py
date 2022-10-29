
from django.contrib import admin
from django.urls import path, include

from . import views

app_name = "services"

urlpatterns = [
    path('', views.list_services, name = 'list_services'),
]
