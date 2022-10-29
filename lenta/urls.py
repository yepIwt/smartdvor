from django.contrib import admin
from django.urls import path

from . import views

app_name = "lenta"

urlpatterns = [
    path('', views.lenta_scroll, name = "lenta_scroll"),
    path('post/create/', views.create_post, name = "create_post"),
    path('post/<int:pk>', views.view_post, name='view_post'),
    path('post/<int:pk>/comments/', views.post_comments, name = "post_comments"),
]
