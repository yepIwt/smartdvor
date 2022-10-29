from http.client import HTTPResponse
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse
from django.contrib.auth.models import User
from core.models import Post, PostComment
from core.forms import PostForm

# Create your views here. Okay.

def lenta_scroll(request):
	posts = Post.objects.all()  
	return render(request, "lenta/list.html", {"posts": posts})

def create_post(request):
	form = PostForm(request.POST or None)
	
	if request.POST and form.is_valid():
		post_title = form.cleaned_data['post_title']
		post_text = form.cleaned_data['post_text']

		u = User.objects.get(username__exact = request.user)
		p = Post(post_title = post_title, post_text = post_text, post_author = u)
		p.save()

		return HttpResponseRedirect(reverse("lenta:view_post", args = [p.id]))
	return render(request,'lenta/creation.html',{'form':form})

def view_post(request, pk):
	try:
		p = Post.objects.get( id = pk )
	except:
		raise Http404("Нет такого поста")
	return render(request, "lenta/page.html", {"post": p})