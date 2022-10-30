from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

def main_page(request):
    return render(request, "pages/main.html")