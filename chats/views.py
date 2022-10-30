from django.shortcuts import render
from .models import *
from .forms import *
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse


# Create your views here. Okay.

def list_chats(request):
	chats = Chat.objects.all()
	return render(request, "chats/list.html", {"chats": chats})

def create_chat(request):

	form = ChatCreate(request.POST or None)
	if request.POST and form.is_valid():

		chat_title = form.cleaned_data['chat_title']

		u = User.objects.get(username__exact = request.user)

		members = f"{u.username}|"
		c = Chat(chat_title = chat_title, members = members)
		c.save()

		return HttpResponseRedirect(reverse("chats:chat_view", args = [c.id]))
	return render(request,'chats/create.html', {'form':form})

def chat_view(request, pk):

	form  = MessageCreate(request.POST or None)

	try:
		c = Chat.objects.get(id = pk)
	except:
		return HttpResponse("<h1> Такого чата не существует. </h1>")
	
	if request.POST and form.is_valid():
		message_text = form.cleaned_data['message_text']
		u = User.objects.get(username__exact = request.user)
		msg = Message(message_author = u, message_text = message_text, where_locate = c)
		msg.save()
		return HttpResponseRedirect(reverse("chats:chat_view", args = [c.id]))
	
	members = c.members.split("|")[:-1]
	msgs = c.message_set.order_by('-id')
	if request.user.username not in members:
		msgs = []
	return render(request, "chats/chat_view.html", {"chat": c, "members": members, "msgs": msgs, "form": form})

def add_user_to_chat(request, pk):

	try:
		c = Chat.objects.get(id = pk)
	except:
		return HttpResponse("<h1> Такого чата не существует. </h1>")
	
	members = c.members.split("|")[:-1]
	if request.user.username in members:
		return HttpResponse("<h1> Вы уже существуете в этом чате. </h1>")
	else:
		members.append(f"{request.user.username}")

	s = "".join([f"{m}|" for m in members])
	c.members = s
	c.save()

	return HttpResponseRedirect(reverse("chats:chat_view", args = [c.id]))
	
	