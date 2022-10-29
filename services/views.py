from django.shortcuts import render
from django.http import HttpResponse
from core.forms import ServiceForm

from django.contrib.auth.models import User

from core.models import Service

# Create your views here.

def list_services(request):
    allservices = Service.objects.all()
    return render(request, "pages/allservices.html", {'services': allservices})