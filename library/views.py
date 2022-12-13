from django.shortcuts import render
from django.http import HttpResponse

# Create your views.py here.

def index(request):
    return HttpResponse("Hello, world. You're at the library index.")