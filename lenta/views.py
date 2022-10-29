from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse
from django.contrib.auth.models import User
from core.models import Post, PostComment
from core.forms import PostForm, CommentForm

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

	form = CommentForm(request.POST or None)

	try:
		p = Post.objects.get( id = pk )
	except:
		raise Http404("Нет такого поста")

	if request.POST and form.is_valid():
		comment_text = form.cleaned_data['comment_text']
		
		u = User.objects.get(username__exact = request.user)
		com = PostComment(post = p, comment_text = comment_text, comment_author = u)
		com.save()
		return HttpResponseRedirect(reverse("lenta:post_comments", args = [pk]))
	
	comments = p.postcomment_set.order_by('-id')
	return render(request, "lenta/page.html", {"post": p, 'form': form, 'comments': comments})

def post_comments(request, pk):

	try:
		p = Post.objects.get( id = pk )
	except:
		raise Http404("Нет такого поста")
	
	comments = p.postcomment_set.order_by('-id')
	return render(request, "lenta/post_comms.html", {"comments": comments, "post": p})